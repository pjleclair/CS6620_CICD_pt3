import requests
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def test_get():
    res = requests.get(BASE_URL)
    assert res.status_code == 200


def test_post():
    res = requests.post(f"{BASE_URL}/coins/bitcoin")
    assert res.status_code == 200
    bad_res = requests.post(f"{BASE_URL}/coins/FAKECOIN")
    assert bad_res.status_code == 400


def test_put():
    res = requests.put(f"{BASE_URL}/coins/FAKECOIN/realCoin")
    assert res.status_code == 200
    bad_res = requests.put(f"{BASE_URL}/coins/")
    assert bad_res.status_code == 404


def test_delete():
    res = requests.delete(f"{BASE_URL}/coins/FAKECOIN")
    assert res.status_code == 200
    bad_res = requests.delete(f"{BASE_URL}/coins/")
    assert bad_res.status_code == 404
