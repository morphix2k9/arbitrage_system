from fastapi import APIRoute

router = APIRouter(prefix="/products", tags=["product_discovery"])

@router.get("/discover")
async def discover_products():
    return {"message": "Discovering trending products..."}