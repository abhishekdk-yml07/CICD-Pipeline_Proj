from fastapi import APIRouter, HTTPException
from typing import List
from .models import Item, ItemResponse

router = APIRouter()

# In-memory store for demo purposes
_items: dict[int, Item] = {}
_next_id = 1


@router.get("/items", response_model=List[ItemResponse], tags=["Items"])
async def list_items():
    return [ItemResponse(id=k, **v.dict()) for k, v in _items.items()]


@router.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def get_item(item_id: int):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse(id=item_id, **_items[item_id].dict())


@router.post("/items", response_model=ItemResponse, status_code=201, tags=["Items"])
async def create_item(item: Item):
    global _next_id
    _items[_next_id] = item
    response = ItemResponse(id=_next_id, **item.dict())
    _next_id += 1
    return response


@router.put("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def update_item(item_id: int, item: Item):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    _items[item_id] = item
    return ItemResponse(id=item_id, **item.dict())


@router.delete("/items/{item_id}", status_code=204, tags=["Items"])
async def delete_item(item_id: int):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_id]
