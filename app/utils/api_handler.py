import requests
from config.config import Config
from utils.logger import logger

def get_api_key(service):
    """Retrieve API key for a specific service from config."""
    api_keys = {
        "google_trends": Config.GOOGLE_TRENDS_API_KEY,  # Now points to SerpApi API key
        "facebook": Config.FACEBOOK_API_KEY,
        "amazon": Config.AMAZON_API_KEY,  # Returns tuple (Access Key ID, Secret Access Key)
        "ebay": Config.EBAY_API_KEY,  # Returns dictionary {app_id, cert_id, dev_id}
        "stockx": Config.STOCKX_API_KEY,
        "zelle": Config.ZELLE_API_KEY,
        "grok": Config.GROK_API_KEY
    }
    key = api_keys.get(service)
    if not key:
        logger.error(f"API key not found for service: {service}")
        raise ValueError(f"API key for {service} is not configured")
    return key

def make_api_request(url, headers=None, method="GET", json=None, params=None):
    """Make a generic API request with error handling."""
    try:
        headers = headers or {}
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json, timeout=10)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.error(f"API request failed for {url}: {str(e)}")
        raise

def make_serpapi_request(endpoint, params=None, method="GET"):
    """Make a specific API request to SerpApi with the API key."""
    serpapi_api_key = get_api_key("google_trends")  # Uses SerpApi API key
    base_url = "https://serpapi.com"
    headers = {"Authorization": f"Bearer {serpapi_api_key}"}

    if params is None:
        params = {}

    # Add required SerpApi parameters (e.g., api_key, engine, q)
    params.update({"api_key": serpapi_api_key, "engine": "google_trends", "q": "electronics,clothing"})  # Example query

    try:
        if method.upper() == "GET":
            response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(f"{base_url}/{endpoint}", headers=headers, json=params, timeout=10)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.error(f"SerpApi request failed for {endpoint}: {str(e)}")
        raise