from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from schemas.note import NoteCreate, NoteUpdate, NoteResponse
from services.note_service import NoteService
from utils.telegram_auth import get_user_id_from_init_data

router = APIRouter(prefix="/api/notes", tags=["notes"])


def verify_user(x_init_data: str = Header(..., alias="X-Init-Data")):
    user_id = get_user_id_from_init_data(x_init_data)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="بيانات التحقق غير صالحة",
        )
    return user_id


@router.get("/", response_model=list[NoteResponse])
def get_notes(
    user_id: int = Depends(verify_user),
    db: Session = Depends(get_db),
):
    return NoteService.get_user_notes(db=db, user_id=user_id)


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    user_id: int = Depends(verify_user),
    db: Session = Depends(get_db),
):
    return NoteService.create_note(db=db, user_id=user_id, note_data=note_data)


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    user_id: int = Depends(verify_user),
    db: Session = Depends(get_db),
):
    note = NoteService.get_note_by_id(db=db, note_id=note_id, user_id=user_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الملاحظة غير موجودة",
        )
    return NoteService.update_note(db=db, note=note, update_data=note_data)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    user_id: int = Depends(verify_user),
    db: Session = Depends(get_db),
):
    note = NoteService.get_note_by_id(db=db, note_id=note_id, user_id=user_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الملاحظة غير موجودة",
        )
    NoteService.delete_note(db=db, note=note)
    return None
