from sqlmodel import Session
from fastapi import HTTPException, status
from app.repositories.auth_repository import AuthRepository
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, verify_refresh_token

class AuthService:
    def __init__(self):
        self.repository = AuthRepository()

    def create_user(
            self,
            session: Session,
            username: str,
            password: str
    ):
        '''
        Cria um novo usuario
        '''
      
        # Verifica se o usuario existe
        user = self.repository.get_user_by_username(
            session, username
        )
        if user:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail='Usuario já existe'
            )
        
        # Gera o hash da senha
        password_hash = hash_password(password)
        
        # Salvando o banco
        new_user = self.repository.create_user(
            session = session,
            username = username,
            password_hash=password_hash
            )
        return new_user
    
    def login(
            self, 
            session: Session, 
            username: str, 
            password: str
    ):
        '''
        Loga um usuario ou sobe erro caso o usurname ou senha estiverem incorretos
        '''
      
        # Verifica se o usuario existe
        user = self.repository.get_user_by_username(
            session, username
        )
        if not user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail='Usuario ou senha invalidos'
            )
        
        # Verifica senha
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Usuario ou senha invalidos'
            )
        
        # Gera o token JWT
        access_token = create_access_token(data={'sub': user.username})

        # Gera o refresh token
        refresh_token = create_refresh_token(data={'sub': user.username})

        # Retorna token
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type':  'bearer'
        }
    
    def refresh_access_token(self, refresh_token: str) -> dict:
        '''
        Recebe um refresh token válido e retorna um novo access token
        '''
        user_data = verify_refresh_token(refresh_token)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token inválido ou expirado'
            )
        
        new_access_token = create_access_token(user_data)
        return {'access_token': new_access_token, 'token_type': 'bearer'}