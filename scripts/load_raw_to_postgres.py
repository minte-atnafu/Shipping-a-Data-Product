import os
import json
import psycopg2
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(filename='load.log', level=logging.INFO)

def load_to_postgres():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('POSTGRES_PORT')
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telegram_messages (
            id SERIAL PRIMARY KEY,
            channel_name VARCHAR,
            message JSONB,
            load_date DATE
        )
    """)
    
    data_dir = 'data/raw/telegram_messages'
    for date_folder in os.listdir(data_dir):
        for channel in os.listdir(os.path.join(data_dir, date_folder)):
            channel_path = os.path.join(data_dir, date_folder, channel)
            for file in os.listdir(channel_path):
                if file.endswith('.json'):
                    with open(os.path.join(channel_path, file)) as f:
                        message = json.load(f)
                        cursor.execute(
                            "INSERT INTO telegram_messages (channel_name, message, load_date) VALUES (%s, %s, %s)",
                            (channel, json.dumps(message), date_folder)
                        )
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Data loaded to PostgreSQL successfully")

if __name__ == '__main__':
    load_to_postgres()