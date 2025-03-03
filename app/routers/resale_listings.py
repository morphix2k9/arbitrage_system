from fastapi import APIRouter

router = APIRouter(prefix="/listings", tags=["resale_listings"])

@router.post("/list")
async def list_products():
    return {"message": "Listing products for resale..."}