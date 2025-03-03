from fastapi import APIRouter

router = APIRouter(prefix="/purchases", tags=["purchase_automation"])

@router.post("/automate")
async def automate_purchases():
    return {"message": "Automating purchases..."}