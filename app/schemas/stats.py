from pydantic import BaseModel

class RatingDistribution(BaseModel):
    rating: int
    quantidade: int

class StatsOverviewResponse(BaseModel):
    '''
    Cria um schema para validar saidas da API de stats Overview
    '''
    total_livros: int
    preco_medio: float
    distribuicao_ratings: list[RatingDistribution]

class StatsCategoriesResponse(BaseModel):
    '''
    Cria um schema para validar saidas da API de stats Categories
    '''
    category: str
    total_livros: int
    preco_medio: float