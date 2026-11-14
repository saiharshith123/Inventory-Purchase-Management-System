from typing import Optional, Literal
from decimal import Decimal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from psycopg2 import IntegrityError
from database import get_conn

app = FastAPI(title="Inventory & Purchase Management API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"],
 allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class SupplierIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: Optional[str] = None
    phone: Optional[str] = None

class ProductIn(BaseModel):
    sku: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=140)
    description: Optional[str] = None
    unit_price: Decimal = Field(default=0, ge=0)
    reorder_level: int = Field(default=10, ge=0)
    supplier_id: Optional[int] = None

class StockChange(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    transaction_type: Literal["RECEIPT", "ISSUE"]
    reference: Optional[str] = None
    notes: Optional[str] = None

@app.get("/")
def home():
    return {
        "message": "Inventory and Purchase Management API is running!",
        "status": "success"
    }

@app.get("/api/suppliers")
def suppliers():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM suppliers ORDER BY name")
        return cur.fetchall()

@app.post("/api/suppliers", status_code=201)
def add_supplier(data: SupplierIn):
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO suppliers(name,email,phone) VALUES(%s,%s,%s) RETURNING *",
                        (data.name,data.email,data.phone))
            return cur.fetchone()
    except IntegrityError:
        raise HTTPException(409, "Supplier email already exists.")

@app.get("/api/products")
def products(search: str = "", supplier_id: Optional[int] = None, low_stock: bool = False):
    sql = """SELECT p.*,s.name AS supplier_name FROM products p
             LEFT JOIN suppliers s ON s.id=p.supplier_id
             WHERE (p.name ILIKE %s OR p.sku ILIKE %s)"""
    params = [f"%{search}%", f"%{search}%"]
    if supplier_id is not None:
        sql += " AND p.supplier_id=%s"
        params.append(supplier_id)
    if low_stock:
        sql += " AND p.quantity <= p.reorder_level"
    sql += " ORDER BY p.name"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

@app.post("/api/products", status_code=201)
def add_product(data: ProductIn):
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""INSERT INTO products(sku,name,description,unit_price,reorder_level,supplier_id)
                VALUES(%s,%s,%s,%s,%s,%s) RETURNING *""",
                (data.sku,data.name,data.description,data.unit_price,data.reorder_level,data.supplier_id))
            return cur.fetchone()
    except IntegrityError:
        raise HTTPException(409, "SKU already exists or supplier does not exist.")

@app.put("/api/products/{product_id}")
def update_product(product_id: int, data: ProductIn):
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""UPDATE products SET sku=%s,name=%s,description=%s,unit_price=%s,
                reorder_level=%s,supplier_id=%s WHERE id=%s RETURNING *""",
                (data.sku,data.name,data.description,data.unit_price,data.reorder_level,data.supplier_id,product_id))
            row = cur.fetchone()
            if not row: raise HTTPException(404, "Product not found.")
            return row
    except IntegrityError:
        raise HTTPException(409, "SKU already exists or supplier does not exist.")

@app.delete("/api/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM products WHERE id=%s RETURNING id", (product_id,))
        if not cur.fetchone(): raise HTTPException(404, "Product not found.")
    # Existing transaction history prevents deletion through the foreign key.

@app.post("/api/stock-transactions", status_code=201)
def stock_change(data: StockChange):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT quantity FROM products WHERE id=%s FOR UPDATE", (data.product_id,))
        row = cur.fetchone()
        if not row: raise HTTPException(404, "Product not found.")
        current = row["quantity"]
        if data.transaction_type == "ISSUE" and current < data.quantity:
            raise HTTPException(400, f"Insufficient stock. Available: {current}")
        updated = current + data.quantity if data.transaction_type == "RECEIPT" else current - data.quantity
        cur.execute("UPDATE products SET quantity=%s WHERE id=%s", (updated,data.product_id))
        cur.execute("""INSERT INTO stock_transactions(product_id,transaction_type,quantity,reference,notes)
            VALUES(%s,%s,%s,%s,%s) RETURNING *""",
            (data.product_id,data.transaction_type,data.quantity,data.reference,data.notes))
        return cur.fetchone()

@app.get("/api/stock-transactions")
def history(product_id: Optional[int] = None):
    sql = """SELECT t.*,p.sku,p.name AS product_name FROM stock_transactions t
             JOIN products p ON p.id=t.product_id"""
    params = []
    if product_id is not None:
        sql += " WHERE t.product_id=%s"
        params.append(product_id)
    sql += " ORDER BY t.created_at DESC LIMIT 200"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql,params)
        return cur.fetchall()

@app.get("/api/dashboard")
def dashboard():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""SELECT COUNT(*) AS product_count,COALESCE(SUM(quantity),0) AS total_units,
            COUNT(*) FILTER(WHERE quantity<=reorder_level) AS low_stock_count FROM products""")
        result = cur.fetchone()
        cur.execute("SELECT id,sku,name,quantity,reorder_level FROM products WHERE quantity<=reorder_level ORDER BY quantity LIMIT 10")
        result["low_stock_items"] = cur.fetchall()
        return result
