from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.db.session import get_session
from app.services.book_service import BookService

router = APIRouter()
service = BookService()

### Rotas de categoria
@router.get('/', response_model=List[str])
def get_all_categories(session: Session = Depends(get_session)):
    '''
    Lista todos as categorias
    ---
    responses: 200
    Exemplo de chamada: /api/v1/categories 
    '''
    return service.list_all_categories(session)
