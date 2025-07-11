import os
import json
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(filename='scrape.log', level=logging.INFO)

async def scrape_channel(client, channel_url, output_dir):
    try:
        entity = await client.get_entity(channel_url)
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_path = os.path.join(output_dir, date_str, entity.title)
        os.makedirs(output_path, exist_ok=True)
        
        async for message in client.iter_messages(entity, limit=300):
            message_data = {
                'id': message.id,
                'date': message.date.isoformat(),
                'text': message.text,
                'has_image': message.photo is not None
            }
            with open(f"{output_path}/{message.id}.json", 'w') as f:
                json.dump(message_data, f)
            if message.photo:
                await message.download_media(f"{output_path}/{message.id}.jpg")
        logging.info(f"Scraped {channel_url} successfully")
    except Exception as e:
        logging.error(f"Error scraping {channel_url}: {str(e)}")

async def main():
    client = TelegramClient('session', 
                          int(os.getenv('TELEGRAM_API_ID')), 
                          os.getenv('TELEGRAM_API_HASH'))
    await client.start()
    channels = ['https://t.me/lobelia4cosmetics', 'https://t.me/tikvahpharma']
    for channel in channels:
        await scrape_channel(client, channel, 'data/raw/telegram_messages')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())