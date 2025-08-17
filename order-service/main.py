from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from prometheus_fastapi_instrumentator import Instrumentator

class Order(BaseModel):
    item: str
    price: float

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Service API"}

def get_conn():
    return mysql.connector.connect(
        host="order-mysql-svc",
        user="root",
        password="rootpass",
        database="lugx_orders"
    )

@app.post("/order")
def place_order(o: Order):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (item, price) VALUES (%s, %s)",
        (o.item, o.price)
    )
    conn.commit()
    conn.close()
    return {"status": "Order placed"}

@app.get("/orders")
def list_orders():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Enable Prometheus metrics to /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
