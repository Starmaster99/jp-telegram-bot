# оставь надежду всяк сюда входящий
# todo: проверять todo перед коммитом

#                                               < +++ БИБЛИОТЕКИ +++ >

import os
import random
import logging
import time

import telebot

from dotenv import load_dotenv
from telebot import types
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#                                 < +++ ОБОЗНАЧЕНИЕ НЕОБХОДИМЫХ ПЕРЕМЕННЫХ +++ >

load_dotenv()   # инициализация .env

logging.basicConfig(filename='log.txt', level=logging.INFO,                                             # параметры
                    format='%(asctime)s : %(levelname)s ::: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')  # логирования

telegroup = os.getenv('GROUP')
KEY = os.getenv('API_KEY')                          # получение .env
bot = telebot.TeleBot(KEY)                          # его использование

logging.info('<---+--->\nStarting new session')     # логирование

chrome_options = Options()                          # настройка запуска хрома в свёрнутом виде
chrome_options.add_argument("--headless")           # подходит для всех версий

driver = webdriver.Chrome(options=chrome_options)   # непосредственно запуск

#                                           < +++ ОБРАБОТКА КОМАНД +++ >


@bot.message_handler(commands=['start'])            # декоратор команды. именно с помощью него работает функция ниже
def start(message):                                 # инициализация функции
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!\n'
                                      'Я - Минако Матсушима, ученица старшей школы. Я учу русский язык уже на '
                                      'протяжении пяти лет. Хоть его я знаю плохо, но упорно стараюсь и учу '
                                      'его каждый день, поэтому некоторые мои реплики могут быть неправильными '
                                      'или некорректными. А ещё я иногда веду себя как робот. Да, и не пиши мне ночью. '
                                      'Я сплю.\nА это весь список моих команд: ', parse_mode='MARKDOWN')
    commands(message)                                                   # вызов ф-ции commands с помощью /commands
    logging.info(f'/start: New user - {message.from_user.username}')    # логирование команды


@bot.callback_query_handler(func=lambda call: True)
def receive(call):
    if call.data == 'dice_repeat':
        dice(call.message)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.reply_to(message, f'Привет, @{message.from_user.username}! Как дела?')
    logging.info(f'{message.from_user.username} typed /hello')


@bot.message_handler(commands=['help'])
def commands(message):
    bot.send_message(message.chat.id, '`< Общая информация >`\n'
                                      '`/help - показывает весь список доступных команд\n`'
                                      '`/info - обо мне`\n\n'
                                      '`< Простейшие команды >\n`'
                                      '`/hello - здоровается с написавшим`\n'
                                      '`/dice - генератор случайных чисел (или D100)`\n'
                                      '`/8ball - шар предсказаний`\n\n'
                                      '`< Поиск >\n`'
                                      '`/search - поиск информации без помощи браузера\n`'
                                      '`/yt - поиск видео на youtube.com\n`'
                                      '`/music - поиск музыки на sefon.pro`', parse_mode="MARKDOWN")
    logging.info(f'{message.from_user.username} typed /commands')


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, 'Привет. Меня зовут Минако Матсушима. Я студентка старшей школы. '
                                      'Я учу русский язык уже пять лет. Мои знания не очень большие, но '
                                      'у меня много русских и украинских друзей. Я хочу практиковаться и '
                                      'учиться больше. Давайте дружить!\nМой день рождения: 24 июля 2004 года.')
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

    driver.get(f"https://www.google.com/")                                          # переход на страницу поиска

    search = message.text.split(" ", 1)[1]                                          # отделение сообщения от команды

    page = driver.find_element_by_xpath("//input[@class='gLFyf gsfi']")             # поиск места для ввода текста
    page.send_keys(search)     # поиск текста
    page.submit()              # Enter
    searchlink = driver.find_element_by_xpath("//div[@class='yuRUbf']/a").get_attribute("href")   # получение результата

    bot.reply_to(message, 'Эта ссылка должна тебе помочь. Когда-нибудь я устану искать за вас информацию...\n'
                          f'{searchlink}', reply_markup=markup)     # выведение результата поиска и добавление кнопки
    logging.info(f'/search: {message.from_user.username} tried to find "{search}".')   # логирование результата


@bot.message_handler(commands=['yt'])
def yt(message):

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('▶️ Найти видео', url='https://www.youtube.com/'))

    search_yt = message.text.split(" ", 1)[1]
    driver.get(f"https://www.youtube.com/results?search_query={search_yt}")

    yt_link = driver.find_element_by_xpath("//a[@id='video-title']").get_attribute("href")

    bot.reply_to(message, f'Держи видео.\n{yt_link}', reply_markup=markup)
    logging.info(f"/yt: {message.from_user.username} tried to find '{search_yt}' video.")


@bot.message_handler(commands=['music'])
def music(message):

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🎵 Найти музыку', url='https://sefon.pro/'))

    search_music = message.text.split(" ", 1)[1]
    driver.get(f"https://sefon.pro/search/?q={search_music}")

    try:

        divhref = driver.find_element_by_xpath("//div[@class='song_name']/a").get_attribute("href")
        divclickable = driver.find_element_by_xpath("//div[@class='song_name']/a").text
        driver.find_element_by_link_text(divclickable).click()

        time.sleep(1)

        date = driver.find_element_by_xpath("//div[@class='list']/p[1]").text
        form = driver.find_element_by_xpath("//div[@class='list']/p[2]").text
        size = driver.find_element_by_xpath("//div[@class='list']/p[4]").text
        dur = driver.find_element_by_xpath("//div[@class='list']/p[5]").text

        bot.reply_to(message, f'Держи песню:\n{divhref}\n{date}\n{form}\n{size}\n{dur}', reply_markup=markup)
        logging.info(f"/music: {message.from_user.username} tried to find '{search_music}' music.")

    except NoSuchElementException:

        bot.reply_to(message, f'Я не смогла найти эту песню 🙁\nПопробуй найти сам', reply_markup=markup)


bot.polling(none_stop=True)
