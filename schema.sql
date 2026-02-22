-- MySQL schema for Product QR Code System
CREATE DATABASE IF NOT EXISTS product_qr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE product_qr;

CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id VARCHAR(50) NOT NULL UNIQUE,
  product_name VARCHAR(255) NOT NULL,
  batch_no VARCHAR(100),
  description TEXT,
  price DECIMAL(12,2),
  company_name VARCHAR(255),
  phone VARCHAR(50),
  website VARCHAR(255),
  email VARCHAR(255),
  address TEXT,
  qr_path VARCHAR(1024),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample seed data (3 products)
INSERT INTO products (product_id, product_name, batch_no, description, price, company_name, phone, website, email, address)
VALUES
('PRD001','Sample Product A','BATCH-A1','A sample product A',12.50,'ExampleCo','+1234567890','https://example.com','sales@example.com','123 Example St'),
('PRD002','Sample Product B','BATCH-B2','A sample product B',25.00,'ExampleCo','+1987654321','https://example.com','info@example.com','456 Example Ave'),
('PRD003','Sample Product C','BATCH-C3','A sample product C',9.99,'ExampleCo','+1122334455','https://example.com','support@example.com','789 Example Blvd');
