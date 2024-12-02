# FastAPI Advantages

# Types and Decorators for Endpoints, Query, Path, Errors
# Automatic JSON Conversion (params, results, request body)
# Automatic Document Generation (http://localhost:8000/docs)
# Works very good together with `pydantic` and 'uvicorn' or 'gunicorn' for multiple requests packages

from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


items = {
    0: Item(name='Hammer', price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name='Pliers', price=5.99, count=15, id=1, category=Category.TOOLS),
    2: Item(name='Nails', price=1.99, count=100, id=2, category=Category.CONSUMABLES),
}


@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}


@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with id {item_id} does not exist."
        )

    return items[item_id]


@app.get("/items/")
def query_item_by_parameters(
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None
) -> dict[str, dict | list[Item]]:
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category == category,
            )
        )

    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }


@app.post("/")
def add_item(item: Item) -> dict[str, Item]:

    if item.id in items:
        raise HTTPException(
            status_code=404, detail=f"Item with id {item.id} already exists."
        )

    items[item.id] = item
    return {
        "added": item
    }


@app.post("/delete/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id in items:
        raise HTTPException(
            status_code=404, detail=f"Item with id {item_id} already exists."
        )
    item = items.pop(item_id)
    return {
        "deleted": item
    }
