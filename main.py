import request_service
from fastapi import FastAPI, HTTPException, status

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    try:
        response = await request_service.get()
        return {"data": response}
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@app.post("/coins/{coin_id}", status_code=status.HTTP_200_OK)
async def get_coin(coin_id: str):
    try:
        response = await request_service.post(coin_id)
        return {"data": response}
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@app.put("/coins/{coin_id}/{text}", status_code=status.HTTP_200_OK)
async def put_coin(coin_id: str, text: str):
    try:
        response = await request_service.put(coin_id, text)
        return {"data": response}
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@app.delete("/coins/{coin_id}", status_code=status.HTTP_200_OK)
async def delete_coin(coin_id: str):
    try:
        response = await request_service.delete(coin_id)
        return {"data": response}
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
