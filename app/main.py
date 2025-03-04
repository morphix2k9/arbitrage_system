from fastapi import FastAPI, HTTPException
from app.routers import product_discovery, price_comparison, seller_outreach, purchase_automation, resale_listings
from utils.logger import logger

app = FastAPI(title="Arbitrage System API")

# Include routers
app.include_router(product_discovery.router)
app.include_router(price_comparison.router)
app.include_router(seller_outreach.router)
app.include_router(purchase_automation.router)
app.include_router(resale_listings.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Arbitrage System API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Arbitrage System API shutting down...")