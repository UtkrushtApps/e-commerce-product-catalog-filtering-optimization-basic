from fastapi import APIRouter, Query
from app.database import get_connection
from app.schemas.schemas import Product, ProductCreate
from typing import List, Optional

router = APIRouter()

@router.get("/products", response_model=List[Product])
def get_products(category_id: Optional[int] = Query(None), brand_id: Optional[int] = Query(None)):
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT id, name, category_id, brand_id, price, description FROM products"
    params = []
    filters = []
    if category_id is not None:
        filters.append("category_id = %s")
        params.append(category_id)
    if brand_id is not None:
        filters.append("brand_id = %s")
        params.append(brand_id)
    if filters:
        sql += " WHERE " + " AND ".join(filters)
    # Inefficient: missing indexes on filter columns; full scan likely
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [Product(id=row[0], name=row[1], category_id=row[2], brand_id=row[3], price=row[4], description=row[5]) for row in rows]

@router.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO products (name, category_id, brand_id, price, description)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, name, category_id, brand_id, price, description
        """,
        (product.name, product.category_id, product.brand_id, product.price, product.description)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return Product(id=row[0], name=row[1], category_id=row[2], brand_id=row[3], price=row[4], description=row[5])