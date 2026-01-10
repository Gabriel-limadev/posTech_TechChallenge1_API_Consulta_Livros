# 📚 Books API

**Books API** é uma API construída com **FastAPI** para consulta de dados de livros.  
O projeto foi desenvolvido como **1° trabalho na Pós em Engenharia de Machine Learning pela FIAP**.

---

## 🌐 API em Produção

A API está disponível em produção no Render:

👉 **https://books-api-j70z.onrender.com/api/v1**

Documentação:

👉 **https://books-api-j70z.onrender.com/docs**

Verificar a saúde da API:

👉 **https://books-api-j70z.onrender.com/api/v1/health**

---

## 🚀 Funcionalidades

- 📖 Listar todos os livros
- 🔎 Buscar livro por ID
- 🏷️ Filtrar livros por título e/ou categoria
- ⭐ Buscar pelos livros com maiores ratings
- 💰 Filtrar por um range de valores
- 📚 Listar todas as categorias
- 📊 Trazer um overview com as métricas principais
- ❤️ Health check da API
- 📄 Documentação automática com Swagger (FastAPI)

---

## 🧱 Arquitetura do Projeto

O projeto segue uma arquitetura simples e organizada, separando responsabilidades:

``` text
Books_API/
├── app/
│   ├── api/                 # Rotas da API
│   │   └── v1/
│   │       ├── endpoints/   # Endpoints (books, categories, health)
│   │       └── router.py    # Router principal
│   │
│   ├── core/
│   │   └── config.py       
|   |   └── security.db     
│   │
│   ├── db/                  # Banco de dados
│   │   └── session.py       # Sessão SQLite
|   |   └── books.db         # Banco SQLite
│   │
│   ├── models/              # Modelos (SQLModel)
│   │   └── auth.py
│   │   └── book.py
│   │
│   ├── repositories/        # Acesso ao banco
│   │   └── auth_repository.py
│   │   └── book_repository.py
│   │
|   ├── schemas/             # Schemas do Banco    
|   |   └── auth.py
|   |   └── book.py
|   |   └── stats.py
|   |
│   ├── services/            # Regras de negócio
│   |   └── auth_service.py
|   |   └── book_service.py
|   |   └── health_service.py
|   |   └── stats_service.py
│   |
|   ├── scraper/             # 🕷️ Coleta de dados
│       └── book_scraper.py
|       └── parser.py
|
├── main.py                  # Inicialização da API
├── pyproject.toml
├── poetry.lock
├── requirements.txt
├── runtime.txt
├── README.md
```

## 📌 Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1` | Informações da API |
| GET | `/api/v1/health` | Verifica se a API está ativa |
| POST | `/api/v1/auth/register` | Responsavel pelo cadastro do usuario |
| POST | `/api/v1/auth/login` | Responsavel pelo login do usuario |
| GET | `/api/v1/books` | Lista todos os livros | 
| GET | `/api/v1/books/{id}` | Busca livro por ID |
| GET | `/api/v1/books/search` | Busca livros por título e/ou categoria |
| GET | `/api/v1/books/top-rated?5` | Busca livros por maiores ratings |
| GET | `/api/v1/books/price-range?min=2&max=10` | Busca livros por range de preço |
| GET | `/api/v1/categories` | Lista todas as categorias |
| GET | `/api/v1/stats/overview` | Lista principais métricas dos livros |
| GET | `/api/v1/stats/categories` | Lista principais métricas das categorias |

---

## 📄 Exemplos de Requests e Responses

### 🔹 Verificar saude da API
**Request**
```http
GET /api/v1/health
```
**Response**
```code
"string"
```

### 🔹 Realizar cadastro
**Request**
```http
POST /api/v1/auth/register
```

### 🔹 Realizar login
**Request**
```http
POST /api/v1/auth/login
```
**Response**
```code
{
    "access_token": str
    "refresh_token": str,
    "token_type": "bearer"
}
```


### 🔹 Buscar todos os livros
**Request**
```http
GET /api/v1/books
```
**Response**
```code
[
   {
     "id": 1,
     "title": "1,000 Places to See Before You Die",
     "price": 26.08,
     "rating": 5,
     "availability": 1,
     "category": "Travel",
     "image": "https://books.toscrape.com/media/cache/9e/10/9e106f81f65b293e488718a4f54a6a3f.jpg"
   }
]
```
### 🔹 Buscar livros por título e/ou categoria
**Request**
```http
GET /api/v1/books/search?title=harry&category=Fantasy
```
**Response**
```code
[
   {
     "id": 327,
     "title": "Harry Potter and the Order of the Phoenix (Harry Potter #5)",
     "price": 31.63,
     "rating": 4,
     "availability": 4,
     "category": "Fantasy",
     "image": "https://books.toscrape.com/media/cache/ca/56/ca565814dfe2d9f73d3d6b1ad7265984.jpg"
   }
]
```
### 🔹 Buscar livro pelo id
**Request**
```http
GET /api/v1/books/2
```
**Response**
```code
[
   {
     "id": 2,
     "title": "1st to Die (Women's Murder Club #1)",
     "price": 53.98,
     "rating": 1,
     "availability": 1,
     "category": "Mystery",
     "image": "https://books.toscrape.com/media/cache/f6/8e/f68e6ae2f9da04fccbde8442b0a1b52a.jpg"
   }
]
```

### 🔹 Buscar livros por maiores ratings
**Request**
```http
GET /api/v1/books/top-rated?5
```
**Response**
```code
[
    {
        "id": 996,
        "title": "Sapiens: A Brief History of Humankind",
        "price": 54.23,
        "rating": 5,
        "availability": 20,
        "category": "History",
        "image": "https://books.toscrape.com/media/cache/ce/5f/ce5f052c65cc963cf4422be096e915c9.jpg"
    },
   ...
]
```

### 🔹 Buscar livros por range de preço
**Request**
```http
GET /api/v1/books/price-range?min=2&max=10
```
**Response**
```code
[
    {
        "id": 362,
        "title": "An Abundance of Katherines",
        "price": 10.0,
        "rating": 5,
        "availability": 5,
        "category": "Young Adult",
        "image": "https://books.toscrape.com/media/cache/9b/c8/9bc86bc10a6beea536422bbe82e076fb.jpg"
    }
]

```

### 🔹 Buscar categorias
**Request**
```http
GET /api/v1/categories
```
**Response**
```code
[
  "string"
]
```

### 🔹 Listar principais métricas dos livros
**Request**
```http
GET /api/v1/stats/overview
```
**Response**
```code
{
    "total_livros": 1000,
    "preco_medio": 35.07034999999999,
    "distribuicao_ratings": [
        {
            "rating": 1,
            "quantidade": 226
        },
       ...
    ]
}
```

### 🔹 Listar principais métricas das categorias
**Request**
```http
GET /api/v1/stats/categories
```

**Response**
```code
[
    {
        "category": "Academic",
        "total_livros": 1,
        "preco_medio": 13.12
    },
    ...
]
```

---

## 🛠 Tecnologias Utilizadas

- **Python**
- **FastAPI**
- **SQLModel**
- **SQLite**
- **Uvicorn**
- **Render (deploy)**
- **Selenium (Web Scraping)**

---

## 🕸️ Web Scraper

Os dados utilizados nesta API foram obtidos por meio de um **web scraper desenvolvido em Python**, responsável por coletar informações de livros como:

- Título
- Categoria
- Preço
- Avaliação
- Disponibilidade

O site utilizado como fonte dos dados foi:

🔗 https://books.toscrape.com/

---

### 📦 Banco de dados (`books.db`)

Para facilitar o uso da API e a avaliação do projeto, o arquivo **`books.db` já está incluído no repositório**.  
Dessa forma, a API pode ser executada imediatamente, sem a necessidade de rodar o scraper.

Essa decisão foi tomada para:
- Simplificar a execução do projeto
- Evitar dependências de scraping durante a execução da API
- Garantir que os dados estejam disponíveis desde o início

O scraper permanece disponível no repositório apenas como etapa opcional de coleta e atualização dos dados.

---

### ▶️ Executando o scraper manualmente

Caso queira **analisar o scraper** basta:

1. Clonar o repositório:
   ```bash
   git clone https://github.com/Gabriel-limadev/Books_API.git
   cd Books_API/app/scraper
   
2. Instalar dependências:
   ```bash
   pip install -r requirements.txt

3. Executar scraper
   ```bash
   python parser.py

---

### ▶️ Executando a API manualmente

Caso queira **Rodar a API em sua máquina local**

1. Clonar o repositório:
   ```bash
   git clone https://github.com/Gabriel-limadev/Books_API.git
   cd Books_API
   
2. Instalar dependências:
   ```bash
   pip install -r requirements.txt

3. Rodar API
   ```bash
   uvicorn app.main:app --reload

A API ficará disponivel localmente em: http://127.0.0.1:8000/api/v1

## 👨‍💻 Autor

Gabriel Lima  
Pós-graduação em Engenharia de Machine Learning — FIAP

