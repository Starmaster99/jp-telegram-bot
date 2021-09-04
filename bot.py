# оставь надежду всяк сюда входящий
# todo: проверять todo перед коммитом

import os
import random
import logging
import telebot

from dotenv import load_dotenv
# from googlesearch import search
from telebot import types
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()                                       # инициализация .env

logging.basicConfig(filename='log.txt', level=logging.INFO,                                             # параметры
                    format='%(asctime)s : %(levelname)s ::: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')  # логирования

KEY = os.getenv('API_KEY')                          # получение .env
bot = telebot.TeleBot(KEY)                          # его использование

logging.info('<---+--->\nStarting new session')     # логирование

chrome_options = Options()                          # настройка запуска хрома в свёрнутом виде
chrome_options.add_argument("--headless")           # подходит для всех версий

driver = webdriver.Chrome(options=chrome_options)   # непосредственно запуск


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!\n'
                                      'Я - Минако Матсушима, ученица старшей школы. Я учу русский язык уже на '
                                      'протяжении пяти лет. Хоть его я знаю плохо, но упорно стараюсь и учу '
                                      'его каждый день, поэтому некоторые мои реплики могут быть неправильными '
                                      'или некорректными. А ещё я иногда веду себя как робот. Да, и не пиши мне ночью. '
                                      'Я сплю.\nА это весь список моих команд: ', parse_mode='MARKDOWN')
    commands(message)
    logging.info(f'/start: New user - {message.from_user.username}')


@bot.callback_query_handler(func=lambda call: True)
def receive(call):
    if call.data == 'dice_repeat':
        dice(call.message)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.reply_to(message, f'Привет, @{message.from_user.username}! Как дела?')
    logging.info(f'{message.from_user.username} typed /hello')


@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id, '`/commands - показывает весь список доступных команд\n`'
                                      '`/info - обо мне`\n'
                                      '`/hello - здоровается с написавшим`\n'
                                      '`/dice - генератор случайных чисел (или D100)`\n'
                                      '`/8ball - шар предсказаний`\n'
                                      '`/search - ищет информацию без помощи браузера`', parse_mode="MARKDOWN")
    logging.info(f'{message.from_user.username} typed /commands')


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, 'Привет. Меня зовут Минако Матсушима. Я студентка старшей школы. '
                                      'Я учу русский язык уже пять лет. Мои знания не очень большие, но '
                                      'у меня много русских и украинских друзей. Я хочу практиковаться и '
                                      'учиться больше. Давайте дружить!')
    logging.info(f'{message.from_user.username} typed /info')


@bot.message_handler(commands=['dice'])
def dice(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='🎲 Кинуть кубик ещё раз', callback_data='dice_repeat')
    markup.add(btn)
    dicenum = str(random.randint(0, 100))
    bot.send_message(message.chat.id, f'_Минако кинула 100-гранный кубик_\n'
                                      f'Число {dicenum} показалось на его верхней грани',
                     parse_mode='MARKDOWN', reply_markup=markup)
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
def search_func(message):

    markup = types.InlineKeyboardMarkup()                                           # инициализация кнопки
    markup.add(types.InlineKeyboardButton('⌨ Загуглить', url='google.com'))         # поиска снизу

    driver.get("https://www.google.com/")                                           # переход на сайт поиска
    search = message.text.split()[-1]                                               # отделение сообщения от команды

    driver.get(f"https://www.google.com/search?q={search}")                         # поиск
    searchlinkk = driver.find_element_by_xpath("//div[@class='yuRUbf']")            # получение контейнера
    searchlink = searchlinkk.find_element_by_xpath(".//a").get_attribute("href")    # получение ссылки из контейнера

    bot.reply_to(message, 'Эта ссылка должна тебе помочь. Когда-нибудь я устану искать за вас информацию...\n'
                          f'{searchlink}', reply_markup=markup)     # выведение результата поиска и добавление кнопки


bot.polling(none_stop=True)
