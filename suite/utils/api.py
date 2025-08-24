import requests
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=100, ttl=3*60*60)

@cached(cache)
def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()['rates'][target_currency]
    except requests.RequestException:
        return None