from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.schemas import TokenData

router = APIRouter()


@router.get("/admin")
async def admin_only(token_data: TokenData = Depends(get_current_user)):
    if token_data.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return {"message": "Admin access granted"}
