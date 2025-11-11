from fastapi import FastAPI
from fastapi import Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://admin:8R1OFRZnYJMsfAgw3lp0HOAMax8a6MfV@dpg-d49s4kbuibrs73c2gko0-a/igniowski"

# -------------------- Banco de Dados --------------------
def get_db():
    conn = None
    try:
        # Tenta estabelecer a conexão
        conn = psycopg2.connect(DATABASE_URL)
        yield conn
    except psycopg2.Error as e:
        # Lança exceção se a conexão falhar
        raise HTTPException(status_code=500, detail=f"Erro de conexão com o banco de dados: {e}")
    finally:
        # Garante que a conexão seja fechada
        if conn:
            conn.close()

# -------------------- FastAPI App --------------------
app = FastAPI(
    title="API de Consulta Livros",
    description="Serviço simples de consulta de livros",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # Ou ["*"] para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/livros")
def listar_livros(db: psycopg2.connect = Depends(get_db)):
    with db.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT titulo, preco FROM livros")
        livros = cur.fetchall()
    return livros

@app.get("/livro/{nome}")
def get_livro(nome: str, db: psycopg2.connect = Depends(get_db)):
    with db.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT titulo, preco, disponibilidade, avaliacao, pagina FROM livros WHERE titulo = %s", (nome,))
        livro = cur.fetchone()

    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro