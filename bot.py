# оставь надежду всяк сюда входящий
# todo: проверять todo перед коммитом

import os
import random
import logging
import telebot

from dotenv import load_dotenv
from googlesearch import search

load_dotenv()

logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s : %(levelname)s ::: %(message)s')

KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(KEY)

logging.info('\n<---+--->\nStarting new session')


@bot.message_handler(commands=['hello'])
def greet(message):
    bot.reply_to(message, f'Привет, @{message.from_user.username}! Как дела?')
    logging.info(f'{message.from_user.username} typed /hello')


@bot.message_handler(commands=['commands', 'start'])
def helpme(message):
    bot.send_message(message.chat.id, '`/commands - показывает весь список доступных команд\n`'
                                      '`/info - обо мне`\n'
                                      '`/hello - здоровается с написавшим`\n'
                                      '`/dice - генератор случайных чисел (или D100)`\n'
                                      '`/8ball - шар предсказаний`\n'
                                      '`/search - ищет информацию без помощи браузера`', parse_mode="MARKDOWN")
    logging.info(f'{message.from_user.username} typed /commands')


@bot.message_handler(commands=['info'])
def about(message):
    bot.send_message(message.chat.id, 'Привет. Меня зовут Минако Матсушима. Я студентка старшей школы. '
                                      'Я учу русский язык уже пять лет. Мои знания не очень большие, но '
                                      'у меня много русских и украинских друзей. Я хочу практиковаться и '
                                      'учиться больше. Давайте дружить!')
    logging.info(f'{message.from_user.username} typed /info')


@bot.message_handler(commands=['dice'])
def dice(message):
    dicenum = str(random.randint(0, 100))
    bot.send_message(message.chat.id, f'Ты кинул кубик и тебе выпало число под номером {dicenum}!')
    logging.info(f'/dice: {message.from_user.username} got {dicenum}.')


@bot.message_handler(commands=['8ball'])
def eightball(message):
    randomlist = ['говорит "да"', 'уверен в правоте этой фразы', 'не сомневается в истинне', 'уверяет тебя в правде',
                  'не уверен в правильности', 'говорит "скорее всего"', 'почти уверен', 'не до конца уверен',
                  'не знает', 'просит повторить', 'не может предсказать', 'не понимает вопроса',
                  'говорит "нет"', 'сообщает "лучше тебе не знать"', 'уверен в ответе "нет"', 'говорит о знаках, и '
                                                                                              'они указывают на "нет"']
    randomphrase = random.choice(randomlist)
    bot.reply_to(message, 'О, великий шар предсказаний! Открой нам глаза и покажи истинну!\n'
                          '_Минако смотрит в шар_\n'
                          f'Шар {randomphrase}.', parse_mode='MARKDOWN')
    logging.info(f'/8ball: {message.from_user.username} typed {message.text} and got "{randomphrase}" phrase.')


@bot.message_handler(commands=['search'])
def search_info(message):
    searchres = ""
    query = message.text
    for searchres in search(query, tld='com', lang='ru', num=1, stop=1):
        searchres = str(searchres)                                      # я понятия не имею что я имел в виду
    bot.reply_to(message, 'Эта ссылка должна тебе помочь. Когда-нибудь я устану искать за вас информацию...\n'
                          f'{searchres}')
    logging.info(f'/search: {message.from_user.username} tried to find {message.text}')
    # работает
    # и на том спасибо


bot.polling()
