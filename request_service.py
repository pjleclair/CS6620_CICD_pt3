from fastapi import HTTPException
import requests
from starlette.status import HTTP_400_BAD_REQUEST
import ujson

BASE_URL = "https://api.coingecko.com/api/v3/coins"


async def get():
    res = requests.get(f"{BASE_URL}/list")
    checkError(res)
    response = ujson.loads(res.text)
    return response


async def post(coin_id: str):
    res = requests.get(f"{BASE_URL}/{coin_id}")
    checkError(res)
    response = ujson.loads(res.text)
    return response


async def put(coin_id: str):
    # This is a fake endpoint, we're just going to return an object
    if coin_id == "":
        raise HTTPException(HTTP_400_BAD_REQUEST)
    return f"{coin_id} created!"


async def delete(coin_id: str):
    if coin_id == "":
        raise HTTPException(HTTP_400_BAD_REQUEST)
    return f"{coin_id} deleted!"


def checkError(response):
    response.raise_for_status()
