import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

# 1. Setup & Configuration
load_dotenv()
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Channels to scrape
channels = [
    'CheMed1', 
    'lobelia4cosmetics', 
    'tikvahpharma'
]

# Ensure directories exist
os.makedirs('logs', exist_ok=True)
os.makedirs('data/raw/images', exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename='logs/scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def scrape_channel(client, channel_username):
    logging.info(f"Started scraping {channel_username}")
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        
        # Create image directory for the channel
        image_dir = f'data/raw/images/{channel_username}'
        os.makedirs(image_dir, exist_ok=True)
        
        scraped_data = []

        async for message in client.iter_messages(entity, limit=100): # Adjust limit as needed
            media_path = None
            if message.photo:
                filename = f"{message.id}.jpg"
                media_path = os.path.join(image_dir, filename)
                await client.download_media(message.photo, media_path)
            
            data = {
                'message_id': message.id,
                'channel_title': channel_title,
                'channel_username': channel_username,
                'message_date': message.date.isoformat(),
                'message_text': message.message,
                'has_media': message.photo is not None,
                'media_path': media_path,
                'views': message.views,
                'forwards': message.forwards
            }
            scraped_data.append(data)

        # Save to Data Lake with Partitioned Structure
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_dir = f'data/raw/telegram_messages/{date_str}'
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = f"{output_dir}/{channel_username}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=4, ensure_ascii=False)
            
        logging.info(f"Successfully saved {len(scraped_data)} messages from {channel_username}")

    except Exception as e:
        logging.error(f"Error scraping {channel_username}: {str(e)}")

async def main():
    async with TelegramClient('scraping_session', api_id, api_hash) as client:
        for channel in channels:
            await scrape_channel(client, channel)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())