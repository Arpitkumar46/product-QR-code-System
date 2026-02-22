import os
from fastapi import FastAPI, Depends, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.templating import Jinja2Templates
from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

from . import db, crud
from .schemas import ProductCreate, ProductOut
from .qr_utils import save_qr_file, generate_qr_bytes

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')
QR_FOLDER = os.getenv('QR_FOLDER', 'static/qrcodes')
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'change_me_please')

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='app/templates')
security = HTTPBasic()

def check_admin(creds: HTTPBasicCredentials = Depends(security)):
    correct_user = creds.username == ADMIN_USER
    correct_pass = creds.password == ADMIN_PASS
    if not (correct_user and correct_pass):
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True

def get_db_dep():
    yield from db.get_db()

@app.get('/product/{product_id}', response_class=HTMLResponse)
def product_page(request: Request, product_id: str, db: Session = Depends(get_db_dep)):
    product = crud.get_by_product_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    # jinja template expects product attributes
    return templates.TemplateResponse('product.html', {'request': request, 'product': product})

@app.get('/product/{product_id}/vcard')
def download_vcard(product_id: str, db: Session = Depends(get_db_dep)):
    product = crud.get_by_product_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404)
    lines = [
        'BEGIN:VCARD',
        'VERSION:3.0',
        f"FN:{product.product_name or ''}",
        f"ORG:{product.company_name or ''}",
    ]
    if product.phone:
        lines.append(f'TEL;TYPE=WORK,VOICE:{product.phone}')
    if product.email:
        lines.append(f'EMAIL:{product.email}')
    if product.address:
        lines.append(f'ADR:;;{product.address};;;;')
    if product.description:
        lines.append(f'NOTE:{product.description}')
    lines.append('END:VCARD')
    vcard = '\n'.join(lines)
    filename = f"{product.product_id}.vcf"
    return Response(content=vcard, media_type='text/vcard', headers={
        'Content-Disposition': f'attachment; filename="{filename}"'
    })

@app.get('/product/{product_id}/pdf')
def download_pdf(product_id: str):
    # Optional/placeholder: implement with reportlab if desired
    raise HTTPException(status_code=501, detail='PDF export not implemented')

@app.post('/admin/products', dependencies=[Depends(check_admin)])
def create_product(payload: ProductCreate, db: Session = Depends(get_db_dep)):
    existing = crud.get_by_product_id(db, payload.product_id)
    if existing:
        raise HTTPException(status_code=400, detail='product_id already exists')
    url = f"{BASE_URL}/product/{payload.product_id}"
    qr_path = save_qr_file(url, payload.product_id, QR_FOLDER)
    data = payload.dict()
    data['qr_path'] = qr_path
    product = crud.create_product(db, data)
    return product

@app.get('/admin', response_class=HTMLResponse, dependencies=[Depends(check_admin)])
def admin_index(request: Request, q: str = None, db: Session = Depends(get_db_dep)):
    products = crud.list_products(db, limit=100, search=q)
    return templates.TemplateResponse('admin.html', {'request': request, 'products': products, 'q': q})

@app.get('/admin/qr-history', dependencies=[Depends(check_admin)])
def qr_history(db: Session = Depends(get_db_dep)):
    items = crud.last_50(db)
    return items

@app.get('/admin/products/{product_id}/download_qr', dependencies=[Depends(check_admin)])
def download_qr(product_id: str, db: Session = Depends(get_db_dep)):
    p = crud.get_by_product_id(db, product_id)
    if not p or not p.qr_path:
        raise HTTPException(status_code=404)
    return FileResponse(path=p.qr_path, media_type='image/png', filename=f'{product_id}.png')

@app.get('/admin/products/{product_id}/delete', dependencies=[Depends(check_admin)])
def delete_product(product_id: str, db: Session = Depends(get_db_dep)):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404)
    return RedirectResponse(url='/admin', status_code=303)
