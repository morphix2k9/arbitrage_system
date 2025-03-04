import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use SerpApi API key for Google Trends-like functionality
    GOOGLE_TRENDS_API_KEY = os.getenv("SERPAPI_API_KEY")  # Updated to use SerpApi API key
    FACEBOOK_API_KEY = os.getenv("FACEBOOK_API_KEY")
    AMAZON_API_KEY = (os.getenv("AMAZON_ACCESS_KEY_ID"), os.getenv("AMAZON_SECRET_ACCESS_KEY"))  # Tuple for Access Key ID and Secret
    EBAY_API_KEY = {
        "app_id": os.getenv("EBAY_APP_ID"),
        "cert_id": os.getenv("EBAY_CERT_ID"),
        "dev_id": os.getenv("EBAY_DEV_ID")
    }  # Dictionary for eBay keyset
    STOCKX_API_KEY = os.getenv("STOCKX_API_KEY")
    ZELLE_API_KEY = os.getenv("ZELLE_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")  # Placeholder for Grok 3
    MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.28))