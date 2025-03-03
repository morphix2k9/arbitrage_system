from fastapi import FastAPI
from app.routers import product_discovery, price_comparison, seller_outreach, purchase_automation, resale_listings

app = FastAPI(title="Arbitrage System API")

# Include routers
app.include_router(product_discovery.router)
app.include_router(price_comparison.router)
app.include_router(seller_outreach.router)
app.include_router(purchase_automation.router)
app.include_router(resale_listings.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Arbitrage System API"}