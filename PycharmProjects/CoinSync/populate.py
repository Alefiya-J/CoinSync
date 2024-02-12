import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CoinSync.settings")

# Configure Django settings
django.setup()
import json
from dashboard.models import CurrencyConversion, Currency, Cryptocurrency, Categories


def populate_exchange(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

        for item in data:
            CurrencyConversion.objects.create(
                from_currency=item['from'],
                to_currency=item['to'],
                rate=item['rate']
            )

def populate_currency(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

        for item in data:
            Currency.objects.create(
                name=item['name'],
                code=item['code'],
                symbol=item['symbol']
            )

def populate_coins(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

        for item in data:
            Cryptocurrency.objects.create(
                symbol=item['symbol'],
                name=item['name'],
                image=item['image'],
                current_price=item['current_price'],
                market_cap=item['market_cap'],
                market_cap_rank=item['market_cap_rank'],
                total_volume=item['total_volume'],
                price_change_percentage_24h=item['price_change_percentage_24h'],
            )

def populate_categories(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

        for item in data:
            Categories.objects.create(
                name=item['name'],
                image=item['image'],
                market_cap=item['market_cap'],
                market_cap_change_24h=item['market_cap_change_24h'],
                content=item['content'],
                coin1=item['coin1'],
                coin2=item['coin2'],
                coin3=item['coin3'],
                volume_24h=item['volume_24h'],
            )

if __name__ == '__main__':
    exchange_file = 'dashboard/static/dashboard/json/exchange.json'
    currency_file = 'dashboard/static/dashboard/json/currencies.json'
    coins_file = 'dashboard/static/dashboard/json/coins.json'
    categories_file = 'dashboard/static/dashboard/json/categories.json'
    populate_exchange(exchange_file)
    populate_currency(currency_file)
    populate_coins(coins_file)
    populate_categories(categories_file)
