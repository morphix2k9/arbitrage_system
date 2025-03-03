from fastapi import APIRouter

router = APIRouter(prefix="/sellers", tags=["seller_outreach"])

@router.post("/negotiate")
async def negotiate_sellers():
    return {"message": "Negotiating with sellers..."}