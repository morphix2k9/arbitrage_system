from fastapi import APIRouter, HTTPException
import requests
import pandas as pd
from config.config import Config
from utils.api_handler import get_api_key, make_api_request
from utils.logger import logger
from utils.rate_limiter import rate_limit

router = APIRouter(prefix="/products", tags=["product_discovery"])

@router.get("/discover")
@rate_limit(max_calls=10, time_frame=60)  # Limit to 10 calls per minute
async def discover_products():
    try:
        google_trends_api_key = get_api_key("google_trends")
        amazon_api_key = get_api_key("amazon")
        ebay_api_key = get_api_key("ebay")
        tiktok_api_key = get_api_key("tiktok")

        # Fetch Google Trends data
        trends_url = f"https://trends.google.com/trends/api/explore?hl=en-US&tz=420&req=%7B%22comparisonItem%22:%5B%7B%22keyword%22:%22electronics%22%7D,%7B%22keyword%22:%22clothing%22%7D%5D%7D"
        trends_headers = {"Authorization": f"Bearer {google_trends_api_key}"}
        trends_data = make_api_request(trends_url, headers=trends_headers)
        logger.info("Fetched Google Trends data")

        # Mock Amazon, eBay, TikTok Shop data (replace with real APIs)
        amazon_data = pd.DataFrame({
            "product": ["Smartphone", "Laptop", "Sneakers"],
            "price": [500, 1000, 100]
        })
        ebay_data = pd.DataFrame({
            "product": ["Smartphone", "Headphones", "Watch"],
            "price": [450, 50, 200]
        })
        tiktok_data = pd.DataFrame({
            "product": ["T-Shirt", "Backpack", "Shoes"],
            "price": [20, 80, 60]
        })

        # Combine and rank products by price (lowest to highest)
        all_products = pd.concat([amazon_data, ebay_data, tiktok_data])
        top_products = all_products.sort_values(by="price").head(10).to_dict(orient="records")

        logger.info(f"Discovered {len(top_products)} trending products")
        return {"products": top_products}

    except requests.RequestException as e:
        logger.error(f"Error fetching trending products: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch trending products")
    except Exception as e:
        logger.error(f"Unexpected error in product discovery: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")