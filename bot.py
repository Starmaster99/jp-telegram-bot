# оставь надежду всяк сюда входящий
# todo: логирование

import os
import logging
import telebot

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s ::: %(message)s')

KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(KEY)


@bot.message_handler(commands=['hello'])
def greet(message):
    bot.reply_to(message, f'Привет, @{message.from_user.username}! Как дела?')
    logging.info(f'{message.from_user.username} typed /hello')


@bot.message_handler(commands=['commands'])
def helpme(message):
    bot.send_message(message.chat.id, '`/commands - показывает весь список доступных команд\n`'
                                      '`/info - обо мне`\n'
                                      '`/hello - здоровается с написавшим`', parse_mode="MARKDOWN")
    logging.info(f'{message.from_user.username} typed /commands')


@bot.message_handler(commands=['info'])
def about(message):
    bot.send_message(message.chat.id, 'Привет. Меня зовут Минако Матсушима. Я студентка старшей школы. '
                                      'Я учу русский язык уже пять лет. Мои знания не очень большие, но '
                                      'у меня много русских и украинских друзей. Я хочу практиковаться и '
                                      'учиться больше. Давайте дружить!')
    logging.info(f'{message.from_user.username} typed /info')


bot.polling()
