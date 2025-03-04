from fastapi import APIRouter, HTTPException
import requests
from config.config import Config
from utils.api_handler import get_api_key, make_api_request
from utils.logger import logger
from utils.rate_limiter import rate_limit

router = APIRouter(prefix="/listings", tags=["resale_listings"])

@router.post("/list")
@rate_limit(max_calls=5, time_frame=60)  # Limit to 5 calls per minute
async def list_products(product: dict):
    try:
        ebay_api_key = get_api_key("ebay")
        amazon_api_key = get_api_key("amazon")
        stockx_api_key = get_api_key("stockx")

        # Mock resale listing on eBay (replace with real API)
        ebay_url = "https://api.ebay.com/v1/listing"
        ebay_headers = {"Authorization": f"Bearer {ebay_api_key}"}
        ebay_payload = {
            "product": product["product"],
            "price": product["resale_price"],
            "platform": "eBay"
        }
        ebay_response = make_api_request(ebay_url, headers=ebay_headers, method="POST", json=ebay_payload)

        # Mock Amazon and StockX listings (similarly replace with real APIs)
        amazon_url = "https://api.amazon.com/v1/listings"
        amazon_headers = {"Authorization": f"Bearer {amazon_api_key}"}
        amazon_payload = ebay_payload.copy()
        amazon_response = make_api_request(amazon_url, headers=amazon_headers, method="POST", json=amazon_payload)

        stockx_url = "https://api.stockx.com/v1/listings"
        stockx_headers = {"Authorization": f"Bearer {stockx_api_key}"}
        stockx_payload = ebay_payload.copy()
        stockx_response = make_api_request(stockx_url, headers=stockx_headers, method="POST", json=stockx_payload)

        logger.info(f"Listed {product['product']} on eBay, Amazon, and StockX at ${product['resale_price']}")
        return {
            "message": "Listing successful",
            "listings": {
                "eBay": ebay_response,
                "Amazon": amazon_response,
                "StockX": stockx_response
            }
        }

    except requests.RequestException as e:
        logger.error(f"Error listing product: {str(e)}")
        raise HTTPException(status_code=500, detail="Listing failed")
    except Exception as e:
        logger.error(f"Unexpected error in resale listing: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")