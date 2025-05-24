import requests
import ujson

class App:

    def main():
        res = requests.get('https://api.coingecko.com/api/v3/coins/list'); 
        response = ujson.loads(res.text);
        print(response);
        return response;
