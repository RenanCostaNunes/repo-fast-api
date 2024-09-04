from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List

class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int

product_storage = []
router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
def get_all_products():
    return product_storage

@router.get("/{product_id}", response_model=ProductSchema)
def get_single_product(product_id: int):
    product = next((item for item in product_storage if item["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def add_new_product(new_product: ProductSchema):
    product_data = new_product.dict()
    product_data['id'] = len(product_storage) + 1
    product_storage.append(product_data)
    return product_data

@router.put("/{product_id}", response_model=ProductSchema)
def modify_product(product_id: int, updated_product: ProductSchema):
    existing_product_index = next((index for index, item in enumerate(product_storage) if item["id"] == product_id), None)
    if existing_product_index is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product_storage[existing_product_index] = updated_product.dict()
    return updated_product.dict()

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(product_id: int):
    global product_storage
    product_index = next((index for index, item in enumerate(product_storage) if item["id"] == product_id), None)
    if product_index is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product_storage.pop(product_index)
    return None
