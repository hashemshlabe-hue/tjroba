from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from schemas.channel import ChannelCreate, ChannelUpdate, ChannelResponse
from services.channel_service import ChannelService
from utils.telegram_auth import get_user_id_from_init_data
from config import settings

router = APIRouter(prefix="/api/admin", tags=["admin"])


def verify_admin(x_init_data: str = Header(..., alias="X-Init-Data")):
    user_id = get_user_id_from_init_data(x_init_data)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="بيانات التحقق غير صالحة",
        )
    if user_id not in settings.ADMIN_IDS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول",
        )
    return user_id


@router.get("/channels", response_model=list[ChannelResponse])
def get_all_channels(
    admin_id: int = Depends(verify_admin),
    db: Session = Depends(get_db),
):
    return ChannelService.get_all_channels(db=db)


@router.post("/channels", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
def create_channel(
    channel_data: ChannelCreate,
    admin_id: int = Depends(verify_admin),
    db: Session = Depends(get_db),
):
    return ChannelService.create_channel(db=db, channel_data=channel_data)


@router.put("/channels/{channel_id}", response_model=ChannelResponse)
def update_channel(
    channel_id: int,
    channel_data: ChannelUpdate,
    admin_id: int = Depends(verify_admin),
    db: Session = Depends(get_db),
):
    channel = ChannelService.get_channel_by_id(db=db, channel_id=channel_id)
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="القناة غير موجودة",
        )
    return ChannelService.update_channel(db=db, channel=channel, update_data=channel_data)


@router.delete("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(
    channel_id: int,
    admin_id: int = Depends(verify_admin),
    db: Session = Depends(get_db),
):
    channel = ChannelService.get_channel_by_id(db=db, channel_id=channel_id)
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="القناة غير موجودة",
        )
    ChannelService.delete_channel(db=db, channel=channel)
    return None
