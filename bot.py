# оставь надежду всяк сюда входящий
# todo: проверять todo перед коммитом

import os
import random
import logging
import telebot

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s : %(levelname)s ::: %(message)s')

KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(KEY)

logging.info('Starting new session')


@bot.message_handler(commands=['hello'])
def greet(message):
    bot.reply_to(message, f'Привет, @{message.from_user.username}! Как дела?')
    logging.info(f'{message.from_user.username} typed /hello')


@bot.message_handler(commands=['commands'])
def helpme(message):
    bot.send_message(message.chat.id, '`/commands - показывает весь список доступных команд\n`'
                                      '`/info - обо мне`\n'
                                      '`/hello - здоровается с написавшим`\n'
                                      '`/dice - генератор случайных чисел (или D100)`\n'
                                      '`/8ball - шар предсказаний (alpha)`', parse_mode="MARKDOWN")
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
    randomlist = ['Да.', 'Нет.']
    randomphrase = random.choice(randomlist)
    bot.reply_to(message, 'О, великий шар предсказаний! Открой нам глаза и покажи истинну!\n'
                          '_Минако смотрит в шар_\n'
                          f'Ответом на твой вопрос является "{randomphrase}"', parse_mode='MARKDOWN')
    logging.info(f'/8ball: {message.from_user.username} got "{randomphrase}" phrase.')


bot.polling()
