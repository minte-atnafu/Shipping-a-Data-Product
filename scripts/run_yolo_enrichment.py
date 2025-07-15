import os
from ultralytics import YOLO
import psycopg2
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(filename='yolo.log', level=logging.INFO)

def run_yolo_enrichment():
    model = YOLO('yolov8n.pt')
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('POSTGRES_PORT')
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_detections (
            id SERIAL PRIMARY KEY,
            message_id VARCHAR,
            detected_object_class VARCHAR,
            confidence_score FLOAT
        )
    """)
    
    data_dir = '../data/raw/telegram_messages/2025-07-11'
    for date_folder in os.listdir(data_dir):
        for channel in os.listdir(os.path.join(data_dir, date_folder)):
            channel_path = os.path.join(data_dir, date_folder, channel)
            for file in os.listdir(channel_path):
                if file.endswith('.jpg'):
                    message_id = file.split('.')[0]
                    results = model(os.path.join(channel_path, file))
                    for result in results:
                        for box in result.boxes:
                            cursor.execute(
                                "INSERT INTO image_detections (message_id, detected_object_class, confidence_score) VALUES (%s, %s, %s)",
                                (message_id, result.names[int(box.cls)], box.conf.item())
                            )
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("YOLO enrichment completed")

if __name__ == '__main__':
    run_yolo_enrichment()