from sqlmodel import Field, SQLModel

class Auth(SQLModel, table=True):
    '''
    Cria o model da tabela de autenticacao
    '''
    __tablename__ = "auth"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, index=True, unique=True)
    password_hash: str = Field(nullable=False)