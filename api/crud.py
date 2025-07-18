
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, text
from . import models
import re
import logging

# Configure logging for debugging
logging.basicConfig(
    filename='api.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_product_name(message_text: str) -> str:
    """
    Extract product name from message_text using regex.
    Assumes product name is at the start of the message, before 'Price' or newline.
    """
    if not message_text:
        logging.warning("Empty message_text received in extract_product_name")
        return "Unknown"
    try:
        match = re.match(r'^\s*(?:[\*\s]*)(.*?)(?:\s*(?:Price|\n|$))', message_text, re.IGNORECASE)
        product_name = match.group(1).strip() if match else "Unknown"
        logging.debug(f"Extracted product name: {product_name} from text: {message_text[:50]}...")
        return product_name
    except Exception as e:
        logging.error(f"Error extracting product name: {str(e)}")
        return "Unknown"

def get_top_products(db: Session, limit: int):
    """
    Retrieve the top products by mention count from fct_messages.
    """
    try:
        # Verify table existence
        db.execute(text("SELECT 1 FROM marts.fct_messages LIMIT 1"))
        logging.debug("Verified marts.fct_messages table exists")
        results = (
            db.query(
                models.Message.product_name.label('product_name'),
                func.count().label('mention_count')
            )
            .filter(models.Message.product_name.isnot(None))
            .group_by(models.Message.product_name)
            .order_by(func.count().desc())
            .limit(limit)
            .all()
        )
        if not results:
            logging.warning("No products found in fct_messages")
            return []
        response = [
            {"product_name": product_name or "Unknown", "mention_count": mention_count}
            for product_name, mention_count in results
        ]
        logging.info(f"Retrieved top {limit} products: {response}")
        return response
    except Exception as e:
        logging.error(f"Error in get_top_products: {str(e)}", exc_info=True)
        raise

def get_channel_activity(db: Session, channel_name: str):
    """
    Retrieve posting activity for a specific channel.
    """
    try:
        # Verify table existence
        db.execute(text("SELECT 1 FROM marts.dim_channels LIMIT 1"))
        logging.debug("Verified marts.dim_channels table exists")
        results = (
            db.query(
                models.Message.message_date,
                func.count().label('message_count')
            )
            .join(models.Channel, models.Message.channel_id == models.Channel.channel_id)
            .filter(models.Channel.channel_name == channel_name)
            .group_by(models.Message.message_date)
            .all()
        )
        if not results:
            logging.warning(f"No activity found for channel: {channel_name}")
            return []
        response = [
            {"message_date": message_date, "message_count": message_count}
            for message_date, message_count in results
        ]
        logging.info(f"Retrieved activity for channel {channel_name}: {response}")
        return response
    except Exception as e:
        logging.error(f"Error in get_channel_activity: {str(e)}", exc_info=True)
        raise

def search_messages(db: Session, query: str):
    """
    Search messages containing a specific keyword.
    """
    try:
        results = (
            db.query(models.Message)
            .filter(models.Message.message_text.ilike(f'%{query}%'))
            .all()
        )
        logging.info(f"Searched messages with query: {query}, found {len(results)} results")
        return results
    except Exception as e:
        logging.error(f"Error in search_messages: {str(e)}", exc_info=True)
        raise