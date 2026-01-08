from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate, UserResponse, TokenResponse

router = APIRouter()
service = AuthService()

# Rota de cadastro
@router.post('/register', response_model=UserResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    '''
    Cria um novo usuario
    '''
    return service.create_user(session, user.username, user.password)

# Rota de login
@router.post('/login', response_model=TokenResponse)
def login(username: str, password: str, session: Session = Depends(get_session)):
    '''
    Realiza login e retorna um token JWT
    '''
    return service.login(session, username, password)

# Rota de Refresh 
@router.post('/refresh', summary='Renova o Access Token')
def refresh_token(refresh_token: str):
    '''
    Atualiza o token
    '''
    return service.refresh_access_token(refresh_token)