from fastapi import FastAPI,Path,Query,HTTPException,status
from typing import Optional
from pydantic import BaseModel

app =  FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {}


@app.get("/")
def home():
    return {"Data":"Test"}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None,description="ID of the inventory Item")):
    return inventory[item_id]

@app.get("/get-by-name")
def get_item(test: int , name: Optional[str] = None):
    for item in inventory:
        if inventory[item]["name"] == name:
            return inventory[item]
    # return {"Data" : "No Match Found"}
    return HTTPException(status_code=404,detail="Item Not Found.")


@app.post("/create-item/{item_id}")
def create_item(item_id:int,item:Item):
    if item_id in inventory:
        return {"Error":"Item ID already exists."}
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id:int, item:UpdateItem):
    if item_id not in inventory:
        return {"Error":"Item ID doesnt exists"}

    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int):
    if item_id not in inventory:
        return{"Error" : "ID not existing"}
    del inventory[item_id]
    return {"Success":"Item Deleted"}