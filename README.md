# Product QR Code System (FastAPI + MySQL)

Minimal runnable scaffold for generating product QR codes, serving product pages, and a simple admin panel.

Prerequisites
- Python 3.10+
- MySQL server

Quick start
1. Create virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create database and user in MySQL, then run schema:

```sql
-- in mysql client
CREATE DATABASE product_qr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'qruser'@'localhost' IDENTIFIED BY 'qrpass';
GRANT ALL ON product_qr.* TO 'qruser'@'localhost';
FLUSH PRIVILEGES;
```

Then run:

```bash
mysql -u qruser -p product_qr < db/schema.sql
```

3. Copy `.env.example` to `.env` and adjust values (DATABASE_URL, BASE_URL, ADMIN_*).

4. Start the app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Admin endpoints
- GET /admin (protected via basic auth) to view products and QR thumbnails
- POST /admin/products to create a product (JSON) — requires basic auth

Public endpoints
- GET /product/{product_id} — product page
- GET /product/{product_id}/vcard — download vCard

Notes
- This scaffold uses a simple HTTP Basic auth for admin protection. For production, put the app behind proper auth or a private network.
- PDF export is left as a placeholder.
