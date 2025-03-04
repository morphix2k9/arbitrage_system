from fastapi import APIRouter, HTTPException
import pandas as pd
from config.config import Config
from utils.logger import logger
from utils.rate_limiter import rate_limit

router = APIRouter(prefix="/prices", tags=["price_comparison"])

@router.get("/compare")
@rate_limit(max_calls=5, time_frame=60)  # Limit to 5 calls per minute
async def compare_prices(products: list = None):
    if not products:
        raise HTTPException(status_code=400, detail="Products list is required")

    try:
        min_margin = Config.MIN_PROFIT_MARGIN  # 0.28 (28%)
        profitable_products = []

        for product in products:
            purchase_price = product.get("price", 0)
            if purchase_price <= 0:
                continue

            # Mock resale prices (replace with real API calls)
            resale_price_ebay = purchase_price * 1.5  # 50% markup
            resale_price_amazon = purchase_price * 1.4  # 40% markup
            resale_price_stockx = purchase_price * 1.6  # 60% markup

            # Calculate margins
            margins = {
                "eBay": (resale_price_ebay - purchase_price) / purchase_price,
                "Amazon": (resale_price_amazon - purchase_price) / purchase_price,
                "StockX": (resale_price_stockx - purchase_price) / purchase_price
            }

            # Filter for minimum margin
            max_margin = max(margins.values())
            if max_margin >= min_margin:
                product["resale_price"] = max(resale_price_ebay, resale_price_amazon, resale_price_stockx)
                product["platform"] = max(margins, key=margins.get)
                profitable_products.append(product)

        logger.info(f"Found {len(profitable_products)} profitable products with >= {min_margin*100}% margin")
        return {"profitable_products": profitable_products}

    except Exception as e:
        logger.error(f"Error comparing prices: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to compare prices")