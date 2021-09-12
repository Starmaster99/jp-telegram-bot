# как узнать chat_id: https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id

import os
import requests
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv('API_KEY')
telegroup = os.getenv('GROUP')

msg = 'Так, дела немного затянулись, продолжим завтра. Не скучайте (￣ε￣)'


def send_msg():
    url = f'https://api.telegram.org/bot{KEY}/sendMessage?chat_id={telegroup}&text={msg}&parse_mode=HTML'
    resp = requests.get(url)
    print(resp)


send_msg()
