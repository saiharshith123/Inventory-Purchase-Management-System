CREATE TABLE IF NOT EXISTS suppliers (
 id SERIAL PRIMARY KEY, name VARCHAR(120) NOT NULL,
 email VARCHAR(160) UNIQUE, phone VARCHAR(30),
 created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS products (
 id SERIAL PRIMARY KEY, sku VARCHAR(50) NOT NULL UNIQUE,
 name VARCHAR(140) NOT NULL, description TEXT,
 unit_price NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK(unit_price >= 0),
 quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
 reorder_level INTEGER NOT NULL DEFAULT 10 CHECK(reorder_level >= 0),
 supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
 created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS stock_transactions (
 id SERIAL PRIMARY KEY, product_id INTEGER NOT NULL REFERENCES products(id),
 transaction_type VARCHAR(10) NOT NULL CHECK(transaction_type IN ('RECEIPT','ISSUE')),
 quantity INTEGER NOT NULL CHECK(quantity > 0), reference VARCHAR(100),
 notes TEXT, created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_transactions_product_date ON stock_transactions(product_id,created_at DESC);
