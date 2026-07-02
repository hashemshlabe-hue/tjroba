from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from schemas.channel import ChannelResponse
from services.channel_service import ChannelService
from models.channel import ChannelType
from utils.telegram_auth import get_user_id_from_init_data

router = APIRouter(prefix="/api/channels", tags=["channels"])


def verify_user(x_init_data: str = Header(..., alias="X-Init-Data")):
    user_id = get_user_id_from_init_data(x_init_data)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="بيانات التحقق غير صالحة",
        )
    return user_id


@router.get("/college", response_model=list[ChannelResponse])
def get_college_channels(db: Session = Depends(get_db)):
    return ChannelService.get_channels_by_type(db=db, channel_type=ChannelType.COLLEGE)


@router.get("/dawah", response_model=list[ChannelResponse])
def get_dawah_channels(db: Session = Depends(get_db)):
    return ChannelService.get_channels_by_type(db=db, channel_type=ChannelType.DAWAH)


@router.get("/groups", response_model=list[ChannelResponse])
def get_groups(db: Session = Depends(get_db)):
    return ChannelService.get_channels_by_type(db=db, channel_type=ChannelType.GROUP)
