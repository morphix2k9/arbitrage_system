from fastapi import APIRouter

router = APIRouter(prefix="/prices", tags=["price_comparison"])

@router.get("/compare")
async def compare_prices():
    return {"message": "Comparing prices for profit margins..."}