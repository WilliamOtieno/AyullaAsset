import requests
from django.conf import settings
from django.contrib.auth.models import User
from .models import PortfolioCoin


def get_top_ranked_currencies() -> list:
    params = {
        "vs_currency": "USD",
        "order": "market_cap_desc",
        "per_page": "10",
        "sparkline": "false",
        "price_change_percentage": "24h",
        "locale": "en"
    }
    url = f"{settings.COINGECKO_BASE_URL}/coins/markets/"
    resp = requests.get(url, params=params)
    res = []
    print({resp.status_code, resp.reason})
    if resp.ok:
        res = resp.json() 
    return res


def search_coin(query: str) -> list:
    params = {"query": query}
    url = f"{settings.COINGECKO_BASE_URL}/search/"
    res = []
    resp = requests.get(url, params=params)
    if resp.ok:
        res = resp.json()["coins"]
    return res


def get_coin_info(coin_id: str) -> dict:
    url = f"{settings.COINGECKO_BASE_URL}/coins/{coin_id}"
    resp = requests.get(url)
    res = {}
    if resp.ok:
        res = dict(resp.json())
    return res


def add_coin_to_user_portfolio(user: User, coin_id: str):
    PortfolioCoin.objects.get_or_create(user=user, coin_id=coin_id)
