from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db
import logging

# Configure logging
logging.basicConfig(
    filename='api.log',
    level=logging.DEBUG,  # Increased to DEBUG for more granularity
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

@app.get("/api/reports/top-products", response_model=list[schemas.ProductReport])
async def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve the top products by mention count.
    """
    try:
        logging.debug(f"Processing top-products request with limit={limit}")
        result = crud.get_top_products(db, limit)
        if not result:
            logging.info("No products found for top-products endpoint")
            return []
        return result
    except Exception as e:
        logging.error(f"Error in top-products endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/channels/{channel_name}/activity", response_model=list[schemas.ChannelActivity])
async def get_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    """
    Retrieve posting activity for a specific channel.
    """
    try:
        logging.debug(f"Processing channel-activity request for channel={channel_name}")
        result = crud.get_channel_activity(db, channel_name)
        if not result:
            logging.info(f"No activity found for channel: {channel_name}")
            raise HTTPException(status_code=404, detail=f"No activity found for channel: {channel_name}")
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error in channel-activity endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/search/messages", response_model=list[schemas.Message])
async def search_messages(query: str, db: Session = Depends(get_db)):
    """
    Search for messages containing a specific keyword.
    """
    try:
        logging.debug(f"Processing search-messages request with query={query}")
        result = crud.search_messages(db, query)
        return result
    except Exception as e:
        logging.error(f"Error in search-messages endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")