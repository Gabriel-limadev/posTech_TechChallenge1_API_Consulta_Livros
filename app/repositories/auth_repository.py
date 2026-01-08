from sqlmodel import Session, select
from app.models.auth import Auth

class AuthRepository:
    
    # Metodo para criação de usuario
    def create_user(
            self,
            session: Session,
            username: str,
            password_hash: str
        ) -> Auth:
        
        user = Auth(username=username, password_hash=password_hash)
        session.add(user)
        session.commit()
        session.refresh(user) 

        return user
    
    def get_user_by_username(
            self, 
            session: Session,
            username: str
    ) -> Auth | None:
        statement = select(Auth).where(Auth.username == username)
        return session.exec(statement).first()