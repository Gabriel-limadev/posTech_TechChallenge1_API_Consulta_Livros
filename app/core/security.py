from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session
from typing import Optional
from datetime import datetime, timedelta, timezone

from app.db.session import get_session
from app.repositories.auth_repository import AuthRepository
from passlib.context import CryptContext
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
ALGORITHM = settings.ALGORITHM


security = HTTPBearer()

pwd_context = CryptContext(
    schemes=['bcrypt_sha256'],
    deprecated='auto'
)

def hash_password(password: str)->str:
    '''
    Gera o hash segura da senha
    '''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)->bool:
    '''
    Verifica se a senha informada corresponde ao hash salvo
    '''
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict)-> str:
    '''
    Cria um token JWT com tempo de expiração
    '''
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    ) 
    to_encode.update({'exp': expire})

    return jwt.encode(
        to_encode, 
        SECRET_KEY, 
        algorithm=ALGORITHM
    )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    '''
    Credencia usuario
    '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    token = credentials.credentials
    try:
        # Decodifica o token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username: str | None = payload.get('sub')
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Busca usuário no banco
    repository = AuthRepository()
    user = repository.get_user_by_username(session, username)

    if user is None:
        raise credentials_exception

    return user

def create_refresh_token(data: dict) -> str:
    '''
    Gera um refresh token de longo prazo
    '''
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_refresh_token(token: str) -> Optional[dict]:
    '''
    Valida o refresh token.
    Retorna os dados do usuário se válido, senão None
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username: 
            return None
        return payload
    except jwt.ExpiredSignatureError:
        # Token expirou
        return None
    except jwt.InvalidTokenError:
        # Token inválido
        return None