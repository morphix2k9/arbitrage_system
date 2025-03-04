import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_TRENDS_API_KEY = os.getenv("GOOGLE_TRENDS_API_KEY")
    FACEBOOK_API_KEY = os.getenv("FACEBOOK_API_KEY")
    AMAZON_API_KEY = os.getenv("AMAZON_API_KEY")
    EBAY_API_KEY = os.getenv("EBAY_API_KEY")
    STOCKX_API_KEY = os.getenv("STOCKX_API_KEY")
    ZELLE_API_KEY = os.getenv("ZELLE_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")  # Placeholder for Grok 3
    MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", 0.28))  # Default 28%