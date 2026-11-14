# Inventory & Purchase Management System

Stack: React + Vite, FastAPI, PostgreSQL.

## Features
- Normalized supplier, product and stock transaction tables.
- Supplier/product create and product update/delete endpoints.
- Stock receipts and issues; rejects issues that exceed available stock.
- Atomic stock update and ledger insert using a PostgreSQL transaction and `SELECT FOR UPDATE`.
- Search, supplier filter and low-stock filter APIs.
- Dashboard summary, low-stock alerts and recent transaction history.
- Pydantic validation and starter tests.

## Requirements
Install Python 3.10+, Node.js 18+, and PostgreSQL 14+.

## 1. Database setup
In pgAdmin Query Tool or psql, create the database:
```sql
CREATE DATABASE inventory_db;
```
Select/connect to `inventory_db`, then execute `backend/schema.sql`, followed by `backend/seed.sql`.
Alternatively, from the project root with psql installed:
```bash
psql -U postgres -d inventory_db -f backend/schema.sql
psql -U postgres -d inventory_db -f backend/seed.sql
```

## 2. Backend setup (Windows PowerShell)
```powershell
cd inventory-purchase-management\backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and enter your PostgreSQL password:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/inventory_db
```
Start the API:
```powershell
uvicorn main:app --reload
```
API: http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

## 3. Frontend setup (open a second terminal)
```powershell
cd inventory-purchase-management\frontend
npm install
npm run dev
```
Open http://localhost:5173.

## 4. Tests
In the backend terminal with its virtual environment active:
```powershell
pytest -q
```
The included tests cover invalid stock quantities and negative prices. Test transactional stock flows against your local PostgreSQL database through Swagger or the UI.

## API endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard` | Summary and low-stock products |
| GET | `/api/products?search=mouse` | Search products |
| GET | `/api/products?low_stock=true` | Low-stock filter |
| GET/POST | `/api/suppliers` | List/create suppliers |
| GET/POST | `/api/products` | List/create products |
| PUT/DELETE | `/api/products/{id}` | Update/delete product |
| POST | `/api/stock-transactions` | Record receipt or issue |
| GET | `/api/stock-transactions` | Transaction history |

Example transaction body:
```json
{"product_id":1,"quantity":5,"transaction_type":"RECEIPT","reference":"PO-1001"}
```

Note: Product deletion is blocked by PostgreSQL if historical transactions refer to it, preserving the audit trail. This starter project does not yet include authentication, pagination, migrations or automated integration tests.
