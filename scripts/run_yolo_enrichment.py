
import os
from ultralytics import YOLO
import psycopg2
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging to track enrichment process and errors
logging.basicConfig(
    filename='yolo.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_yolo_enrichment():
    # Initialize YOLOv8 model (pre-trained)
    model = YOLO('yolov8n.pt')

    # Connect to PostgreSQL database
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            port=os.getenv('POSTGRES_PORT')
        )
        cursor = conn.cursor()

        # Create image_detections table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_detections (
                id SERIAL PRIMARY KEY,
                message_id VARCHAR,
                detected_object_class VARCHAR,
                confidence_score FLOAT
            )
        """)
    except Exception as e:
        logging.error(f"Failed to connect to PostgreSQL or create table: {str(e)}")
        raise

    # Use the specified data directory
    data_dir = os.path.join('..', 'data', 'raw', 'telegram_messages', '2025-07-11')

    # Verify that the data directory exists
    if not os.path.exists(data_dir):
        logging.error(f"Data directory does not exist: {data_dir}")
        raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    # Iterate through channel directories in the specified date folder
    try:
        for channel in os.listdir(data_dir):
            channel_path = os.path.join(data_dir, channel)
            # Ensure channel_path is a directory
            if not os.path.isdir(channel_path):
                logging.warning(f"Skipping non-directory: {channel_path}")
                continue

            # Process only .jpg files in the channel directory
            for file in os.listdir(channel_path):
                if not file.lower().endswith('.jpg'):
                    logging.info(f"Skipping non-image file: {file}")
                    continue

                file_path = os.path.join(channel_path, file)
                # Verify that the file exists
                if not os.path.isfile(file_path):
                    logging.warning(f"Skipping invalid file path: {file_path}")
                    continue

                try:
                    # Extract message_id from filename (e.g., '1.jpg' -> '1')
                    message_id = os.path.splitext(file)[0]

                    # Run YOLOv8 on the image
                    results = model(file_path)
                    for result in results:
                        for box in result.boxes:
                            # Insert detection results into the database
                            cursor.execute(
                                """
                                INSERT INTO image_detections 
                                (message_id, detected_object_class, confidence_score) 
                                VALUES (%s, %s, %s)
                                """,
                                (message_id, result.names[int(box.cls)], box.conf.item())
                            )
                    logging.info(f"Processed image: {file_path}")
                except Exception as e:
                    logging.error(f"Error processing image {file_path}: {str(e)}")
                    continue

        # Commit database changes
        conn.commit()
        logging.info("YOLO enrichment completed successfully")

    except Exception as e:
        logging.error(f"Error during enrichment process: {str(e)}")
        raise
    finally:
        # Close database connections
        cursor.close()
        conn.close()

if __name__ == '__main__':
    run_yolo_enrichment()
