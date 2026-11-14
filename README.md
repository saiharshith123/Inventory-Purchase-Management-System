# Inventory and Purchase Management System
A full-stack web application built to manage inventory, suppliers, product stock, and purchase transactions. The system provides a centralized dashboard to monitor stock levels, track inventory movements, and manage products efficiently.

## 🚀 Project Overview
The Inventory and Purchase Management System helps businesses maintain accurate inventory records and monitor stock availability. Users can manage suppliers and products, record stock receipts and issues, and view transaction history through a simple React-based dashboard.

The backend is developed using FastAPI, with PostgreSQL used for persistent data storage.

## ✨ Features
### Dashboard
- View total products and suppliers.
- Monitor available stock.
- View low-stock alerts.
- Track inventory statistics.

### Supplier Management
- Add new suppliers.
- View supplier details.
- Manage supplier information.

### Product Management
- Add new products.
- View product details and stock quantities.
- Associate products with suppliers.
- Search and filter products.
- Identify products with low stock.

### Stock Management
- Record stock receipts when new inventory arrives.
- Record stock issues when inventory is used or sold.
- Automatically update product stock quantities.
- Prevent stock quantities from becoming negative.

### Transaction History
- Maintain records of stock movements.
- Track stock receipt and issue transactions.
- View previous inventory transactions.

### Database Management
- Store supplier, product, and transaction information in PostgreSQL.
- Use database transactions for stock updates.
- Apply row-level locking to help prevent conflicting stock operations.

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React.js, JavaScript, CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| API Documentation | Swagger UI, OpenAPI |
| Database Connectivity | Psycopg2 |
| Testing | Pytest |
| Development Tools | VS Code, Postman, pgAdmin |

## 📁 Project Structure

```text
inventory-purchase-management/
│
├── backend/
│   ├── .env.example
│   ├── database.py
│   ├── main.py
│   ├── requirements.txt
│   ├── schema.sql
│   ├── seed.sql
│   ├── pytest.ini
│   │
│   └── tests/
│       └── test_validation.py
│
├── frontend/
│   ├── package.json
│   ├── index.html
│   │
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── style.css
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/inventory-purchase-management.git
```

Navigate to the project directory:

```bash
cd inventory-purchase-management
```

### 2. Backend Setup

Navigate to the backend folder:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. PostgreSQL Database Setup

Make sure PostgreSQL is installed and running.

Create a new database:

```sql
CREATE DATABASE inventory_purchase_db;
```

Connect to the database:

```sql
\c inventory_purchase_db
```

Execute the SQL scripts in the following order using pgAdmin Query Tool or PostgreSQL:

1. `backend/schema.sql`
2. `backend/seed.sql`

The schema script creates the required tables, and the seed script inserts sample records.

### 4. Configure Environment Variables

Create a `.env` file inside the `backend` folder.

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/inventory_purchase_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

**Important:** Never upload your actual `.env` file or database credentials to GitHub.

### 5. Start the Backend Server

From the backend directory, run:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger API Documentation:

```text
http://localhost:8000/docs
```

### 6. Frontend Setup

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/api/dashboard` | Retrieve dashboard statistics |
| GET | `/api/suppliers` | Get all suppliers |
| POST | `/api/suppliers` | Add a supplier |
| GET | `/api/products` | Get all products |
| POST | `/api/products` | Add a product |
| GET | `/api/stock-transactions` | Get transaction history |
| POST | `/api/stock-transactions` | Record stock receipt or issue |

For complete request and response details, visit:

`http://localhost:8000/docs`

## 🗄️ Database Tables

The application uses the following main PostgreSQL tables:

### 1. Suppliers
Stores supplier information.

### 2. Products
Stores product details, supplier relationships, stock quantities, and stock thresholds.

### 3. Stock Transactions
Stores inventory movement records, including stock receipts and stock issues.

## 🧪 Testing

Run the backend tests from the backend directory:

```bash
pytest -q
```

## 🔒 Important Implementation Details

- Uses FastAPI for REST API development.
- Uses PostgreSQL for reliable data persistence.
- Uses database transactions for inventory updates.
- Uses `SELECT ... FOR UPDATE` to lock product records during stock operations.
- Validates stock operations to prevent negative inventory.
- Separates frontend, backend, and database responsibilities.

## 📸 Application Screenshots

### Dashboard
<img width="930" height="954" alt="image" src="https://github.com/user-attachments/assets/4013b031-4321-47d7-90f4-806c06b2adbb" />

### Product Management
<img width="1154" height="331" alt="image" src="https://github.com/user-attachments/assets/47484abf-1ab7-484f-ab7d-54bb339430f0" />

### Supplier Management
<img width="569" height="277" alt="image" src="https://github.com/user-attachments/assets/f6501f4e-3869-4d4d-88a9-052afb293e81" />

### Stock Transactions
<img width="1148" height="259" alt="image" src="https://github.com/user-attachments/assets/a9fe1600-abe1-4b5d-ac0c-6ead4c9372d9" />

## 🔮 Future Enhancements

- User authentication and role-based access control.
- Edit and delete functionality for products and suppliers.
- Purchase order creation and management.
- Invoice generation and PDF export.
- Advanced sales and inventory reports.
- Automated low-stock notifications.
- Docker-based deployment.
- Cloud deployment and production configuration.

## 👨‍💻 Author

**B.Sai Harshith**

- GitHub: https://github.com/saiharshith123
- LinkedIn: https://www.linkedin.com/in/bachina-sai-harshith/

## 📄 License

This project is developed for learning and portfolio purposes.
