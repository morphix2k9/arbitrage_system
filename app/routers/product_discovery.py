from fastapi import APIRouter, HTTPException
import pandas as pd
from config.config import Config
from utils.api_handler import get_api_key, make_serpapi_request, make_api_request
from utils.logger import logger
from utils.rate_limiter import rate_limit

router = APIRouter(prefix="/products", tags=["product_discovery"])

@router.get("/discover")
@rate_limit(max_calls=10, time_frame=60)  # Limit to 10 calls per minute
async def discover_products():
    try:
        # Use SerpApi for trending keywords (example for Google Trends-like data)
        params = {
            "engine": "google_trends",  # Use Google Trends engine
            "q": "electronics,clothing",  # Example keywords
            "geo": "US",  # US market, adjust as needed
            "timeframe": "today 12-m"  # Last 12 months, adjust as needed
        }
        serpapi_data = make_serpapi_request("search", params=params)
        logger.info("Fetched SerpApi trend data")

        # Parse SerpApi data into a DataFrame (simplified, adjust based on actual response)
        products = []
        for item in serpapi_data.get("trends", {}).get("items", []):  # Adjust based on SerpApi response structure
            products.append({
                "product": item.get("query", "Unknown Product"),  # Use query or title as product name
                "price": estimate_price(item.get("volume", 0))  # Estimate price based on search volume
            })

        # Mock Amazon, eBay data (replace with real APIs)
        amazon_data = pd.DataFrame({
            "product": ["Smartphone", "Laptop", "Sneakers"],
            "price": [500, 1000, 100]
        })
        ebay_data = pd.DataFrame({
            "product": ["Smartphone", "Headphones", "Watch"],
            "price": [450, 50, 200]
        })

        # Combine and rank products by price (lowest to highest)
        all_products = pd.concat([pd.DataFrame(products), amazon_data, ebay_data])
        top_products = all_products.sort_values(by="price").head(10).to_dict(orient="records")

        logger.info(f"Discovered {len(top_products)} trending products")
        return {"products": top_products}

    except requests.RequestException as e:
        logger.error(f"Error fetching trending products: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch trending products")
    except Exception as e:
        logger.error(f"Unexpected error in product discovery: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

def estimate_price(search_volume):
    """Estimate a price based on search volume (simplified placeholder)."""
    # This is a placeholder; adjust based on your business logic or SerpApi metrics
    if search_volume > 100000:
        return 1000  # High-demand product
    elif search_volume > 10000:
        return 500
    else:
        return 100