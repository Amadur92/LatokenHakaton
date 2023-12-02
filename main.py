from openai import OpenAI
from newsapi import NewsApiClient
from datetime import date
client = OpenAI(api_key='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')
from openai import OpenAI
import autogen



# Замените 'YOUR_API_KEY' на ваш собственный ключ доступа


messages = [ {"role": "system", "content":
              "You are a intelligent assistant."} ]


import requests
from datetime import datetime, timedelta


def price_difference_percentage(price1, price2):
    if price1 == 0 or price2 == 0:
        raise ValueError("Одна из цен равна нулю, невозможно вычислить процентную разницу")

    difference = abs(price1 - price2)
    average_price = (price1 + price2) / 2
    percentage_difference = (difference / average_price) * 100

    return percentage_difference


def get_bitcoin_price_change():
    # CoinGecko API URL
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'

    # Получаем дату сегодня и семь дней назад в формате UNIX
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    params = {
        'vs_currency': 'usd',
        'days': '7',
        'interval': 'daily'
    }

    # Отправка запроса
    response = requests.get(url, params=params)
    data = response.json()

    # Получаем цены за последнюю неделю
    prices = data.get('prices', [])

    # Рассчитываем изменение цены, если данные доступны
    if prices:
        start_price = prices[0][1]  # Цена 7 дней назад
        end_price = prices[-1][1]  # Текущая цена
        price_change = end_price - start_price
        percent_difference = price_difference_percentage(start_price, end_price)
        return price_change, percent_difference
    else:
        print("No data available for the given timeframe.")
        return None


import requests
from datetime import datetime, timedelta

# Замените YOUR_API_KEY на ваш реальный ключ API
API_KEY = 'YOUR_API_KEY'


def get_bitcoin_news():
    # Текущая дата и дата семи дней назад
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Форматирование дат в вид, который необходим API (YYYY-MM-DD)
    end_date = end_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')

    # Базовый URL News API для поиска статей
    url = 'https://newsapi.org/v2/everything'

    # Параметры запроса
    params = {
        'q': 'биткоин',  # Ключевое слово для поиска
        'from': start_date,  # Дата начала поиска
        'to': end_date,  # Дата конца поиска
        'sortBy': 'publishedAt',  # Сортировать по дате публикации
        'apiKey': '25d8bec73be94f0fb0392e3463f8c08b'  # Ваш API ключ
    }

    # Запрос к API
    response = requests.get(url, params=params)
    response_json = response.json()

    if response.status_code == 200:
        result = ""
        # Возвращаем новости, если запрос прошёл успешно
        for article in response_json['articles']:
            result += article['title']
        return result
    else:
        # Возвращаем сообщение об ошибке, если что-то пошло не так
        return f'Error: {response_json["message"]}'


import autogen



config_list = [
    {
        'model': 'gpt-4',
        'api_key': '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',
    }
]
total_assistant = autogen.AssistantAgent(
    name="Summary",
    llm_config={
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,
        "temperature": 0,
    },
)
user_proxy = autogen.UserProxyAgent(
    name="LatokenBitcoinNews",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith(""),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)
user_proxy.initiate_chat(
    total_assistant,
    message=f""" Так изменилась цена биткоина {get_bitcoin_price_change()}
Ты профессиональный криптоаналитик. 
Проанализируй новости {get_bitcoin_news()} и сделай один общий вывод, почему так произошло
Дай ответ на русском языке""",
)