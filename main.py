import request_service
from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_):
    await request_service.initialize_services()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/items", status_code=status.HTTP_200_OK)
async def get_items():
    try:
        response = await request_service.get_all()
        return {"data": response}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(item_id: str):
    try:
        response = await request_service.get(item_id)
        return {"data": response}
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Dict[Any, Any]):
    try:
        response = await request_service.post(item)
        return {"data": response}
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put("/items/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(item_id: str, item: Dict[Any, Any]):
    try:
        response = await request_service.put(item_id, item)
        return {"data": response}
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: str):
    try:
        response = await request_service.delete(item_id)
        return {"data": response}
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
