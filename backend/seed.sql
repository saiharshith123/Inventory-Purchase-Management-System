INSERT INTO suppliers(name,email,phone) VALUES
('North Star Supplies','sales@northstar.test','9876543210'),
('Metro Wholesale','orders@metro.test','9123456780') ON CONFLICT(email) DO NOTHING;
INSERT INTO products(sku,name,description,unit_price,quantity,reorder_level,supplier_id)
SELECT 'KB-001','Wireless Keyboard','USB wireless keyboard',899,24,8,id FROM suppliers
WHERE email='sales@northstar.test' ON CONFLICT(sku) DO NOTHING;
INSERT INTO products(sku,name,description,unit_price,quantity,reorder_level,supplier_id)
SELECT 'MS-002','Optical Mouse','Optical USB mouse',399,5,10,id FROM suppliers
WHERE email='orders@metro.test' ON CONFLICT(sku) DO NOTHING;
