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
    
    data_dir = '../data/raw/telegram_messages/2025-07-11'
    load_date = '2025-07-11'
    if not os.path.exists(data_dir):
      logging.error(f"Data directory not found: {data_dir}")
      print(f"Error: Data directory not found: {data_dir}")
      return

    for channel in os.listdir(data_dir):
        channel_path = os.path.join(data_dir, channel)
        if os.path.isdir(channel_path):
            for file in os.listdir(channel_path):
                if file.endswith('.json'):
                    file_path = os.path.join(channel_path, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            message = json.load(f)
                            cursor.execute(
                                "INSERT INTO telegram_messages (channel_name, message, load_date) VALUES (%s, %s, %s)",
                                (channel, json.dumps(message), load_date)
                            )
                        except Exception as e:
                            logging.error(f"Error processing file {file_path}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Data loaded to PostgreSQL successfully")

if __name__ == '__main__':
    load_to_postgres()
