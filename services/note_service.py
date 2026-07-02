from sqlalchemy.orm import Session
from models.note import Note
from schemas.note import NoteCreate, NoteUpdate


class NoteService:

    @staticmethod
    def get_user_notes(db: Session, user_id: int):
        return (
            db.query(Note)
            .filter(Note.user_id == user_id)
            .order_by(Note.updated_at.desc())
            .all()
        )

    @staticmethod
    def create_note(db: Session, user_id: int, note_data: NoteCreate):
        note = Note(
            user_id=user_id,
            content=note_data.content,
            category=note_data.category,
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def get_note_by_id(db: Session, note_id: int, user_id: int):
        return (
            db.query(Note)
            .filter(Note.id == note_id, Note.user_id == user_id)
            .first()
        )

    @staticmethod
    def update_note(db: Session, note: Note, update_data: NoteUpdate):
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(note, key, value)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def delete_note(db: Session, note: Note):
        db.delete(note)
        db.commit()
