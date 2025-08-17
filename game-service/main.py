from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from prometheus_fastapi_instrumentator import Instrumentator

class Game(BaseModel):
    name: str
    category: str
    release_date: str
    price: float

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Game Service API"}

def get_conn():
    return mysql.connector.connect(
        host="game-mysql-svc",
        user="root",
        password="rootpass",
        database="lugx_games"
    )

@app.post("/games")
def add_game(g: Game):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO games (name, category, release_date, price) VALUES (%s, %s, %s, %s)",
        (g.name, g.category, g.release_date, g.price)
    )
    conn.commit()
    conn.close()
    return {"status": "Game added"}

@app.get("/games")
def list_games():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM games")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Enable Prometheus metrics to /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# test ci-cd
