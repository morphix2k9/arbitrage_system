from fastapi import APIRouter, HTTPException
import requests
from config.config import Config
from utils.api_handler import get_api_key, make_api_request
from utils.logger import logger
from utils.rate_limiter import rate_limit

router = APIRouter(prefix="/sellers", tags=["seller_outreach"])

@router.post("/negotiate")
@rate_limit(max_calls=5, time_frame=60)  # Limit to 5 calls per minute
async def negotiate_sellers(product: dict):
    try:
        facebook_api_key = get_api_key("facebook")
        grok_api_key = get_api_key("grok")  # Placeholder for Grok 3

        # Simulate Facebook Marketplace API call (replace with real integration)
        facebook_url = "https://graph.facebook.com/v12.0/marketplace"
        headers = {"Authorization": f"Bearer {facebook_api_key}"}
        response = make_api_request(facebook_url, headers=headers)

        # Simulate Grok 3 for negotiation (replace with actual Grok 3 API)
        negotiation_url = "https://api.xai.grok/v1/negotiate"  # Hypothetical endpoint
        negotiation_headers = {"Authorization": f"Bearer {grok_api_key}"}
        negotiation_payload = {
            "product": product,
            "target_price": product["price"] * 0.9  # Negotiate 10% discount
        }
        negotiation_response = make_api_request(negotiation_url, headers=negotiation_headers, method="POST", json=negotiation_payload)

        deal_price = negotiation_response.get("deal_price", product["price"] * 0.9)
        logger.info(f"Negotiated deal for {product['product']} at ${deal_price}")
        return {"message": "Negotiation successful", "deal_price": deal_price}

    except requests.RequestException as e:
        logger.error(f"Error negotiating with seller: {str(e)}")
        raise HTTPException(status_code=500, detail="Negotiation failed")
    except Exception as e:
        logger.error(f"Unexpected error in seller negotiation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")