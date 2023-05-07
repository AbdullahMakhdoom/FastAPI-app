from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello World"}

# Path parameters
""" @app.get("/items/{items_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
"""

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# Query parameters
""" 
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit] 
"""

@app.get("/items_query/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Request Body
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/create_items/{item_id}")
async def create_items(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# 6 - String validation of Query Parameters

""" @app.get("/items/")
async def read_items(
    q: Annotated[str | None,
                Query(
                    alias="item-query",
                    title="Query string",
                    description="Query string for the items to search in the database that have a good match",
                    min_length=3,
                    max_length=50,
                    regex="^fixedquery$",
                    deprecated=True,
                    ),
                ] = None):
    results = {"items": [{"items_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

 
@app.get("/items_list/")
async def read_items_list(q: Annotated[list[str] | None, Query()] = None):
    results = {"items": [{"items_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
"""

# 7 - Path Validation
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=1, le=1000)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results