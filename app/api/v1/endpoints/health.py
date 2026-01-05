from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.services.health_service import HealthService

router = APIRouter()
service = HealthService()

### Rotas sobre a saude da API
@router.get('/')
def health_check(session: Session = Depends(get_session)):
    '''
    Retorna a saude do sistema
    ---
    responses: 200
    Exemplo de chamada: /api/v1/health 
    '''
    return service.check_health(session)
