from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from db.session import get_session
from services.book_service import BookService

router = APIRouter()
service = BookService()

@router.get('/', response_model=List[str])
def get_all_categories(session: Session = Depends(get_session)):
    return service.list_all_categories(session)
