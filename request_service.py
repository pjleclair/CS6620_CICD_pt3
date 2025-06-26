from fastapi import HTTPException
import requests
from starlette.status import HTTP_400_BAD_REQUEST
import ujson

BASE_URL = "https://api.coingecko.com/api/v3/coins"

db = {}


async def get():
    res = requests.get(f"{BASE_URL}/list")
    checkError(res)
    response = ujson.loads(res.text)
    return response


async def post(coin_id: str):
    res = requests.get(f"{BASE_URL}/{coin_id}")
    checkError(res)
    response = ujson.loads(res.text)
    db[coin_id] = res.text
    return response


async def put(coin_id: str, text: str):
    # This is a fake endpoint, we're just going to return a string
    # Note that FastAPI will throw a 404 with empty id string, this is a backup
    if coin_id == "":
        raise HTTPException(HTTP_400_BAD_REQUEST)
    db[coin_id] = text
    return f"{coin_id} updated!"


async def delete(coin_id: str):
    # This is a fake endpoint, we're just going to return a string
    # Note that FastAPI will throw a 404 with empty id string, this is a backup
    if coin_id == "":
        raise HTTPException(HTTP_400_BAD_REQUEST)
    del db[coin_id]
    return f"{coin_id} deleted!"


def checkError(response):
    response.raise_for_status()
