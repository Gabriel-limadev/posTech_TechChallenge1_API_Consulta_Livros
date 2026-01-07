import pandas as pd
from sqlalchemy import create_engine, String, Float, Integer
from book_scraper import BookScraper
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # Books_API/
DB_PATH = BASE_DIR / 'app' / 'db' / 'books.db'


# Instancia o scraper responsável por coletar os dados dos livros
scraper = BookScraper()

try:
    # Executa o scraping completo e retorna uma as informações de todos os livros    
    books_data = scraper.scrape_all_books()

finally:
    scraper.close()


# Converte a lista de dicionários em um DataFrame do pandas
df = pd.DataFrame(books_data)


# Cria uma conexão com o banco de dados
engine = create_engine(f"sqlite:///{DB_PATH}")

df['price'] = (
    df['price']
    .str.replace('£', '', regex=False)
    .astype(float)
)

df['rating'] = df['rating'].astype(int)

# Salva o DataFrame na tabela books
df.to_sql(
    'books',
    engine,
    if_exists='replace',
    index=False,
    dtype={
        'title': String(255),
        'price': Float(),
        'rating': Integer(),
        'category': String(100),
        'availability': String(50)
    }
)