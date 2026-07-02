from sqlalchemy.orm import Session
from models.channel import Channel, ChannelType
from schemas.channel import ChannelCreate, ChannelUpdate


class ChannelService:

    @staticmethod
    def get_channels_by_type(db: Session, channel_type: ChannelType):
        return (
            db.query(Channel)
            .filter(Channel.type == channel_type, Channel.is_active == True)
            .order_by(Channel.name.asc())
            .all()
        )

    @staticmethod
    def get_all_channels(db: Session):
        return db.query(Channel).order_by(Channel.type.asc(), Channel.name.asc()).all()

    @staticmethod
    def create_channel(db: Session, channel_data: ChannelCreate):
        channel = Channel(
            name=channel_data.name,
            link=channel_data.link,
            type=channel_data.type,
            description=channel_data.description,
        )
        db.add(channel)
        db.commit()
        db.refresh(channel)
        return channel

    @staticmethod
    def get_channel_by_id(db: Session, channel_id: int):
        return db.query(Channel).filter(Channel.id == channel_id).first()

    @staticmethod
    def update_channel(db: Session, channel: Channel, update_data: ChannelUpdate):
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(channel, key, value)
        db.commit()
        db.refresh(channel)
        return channel

    @staticmethod
    def delete_channel(db: Session, channel: Channel):
        db.delete(channel)
        db.commit()
