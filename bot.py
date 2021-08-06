# оставь надежду всяк сюда входящий


import telebot

bot = telebot.TeleBot('')  # sorry :P


@bot.message_handler(commands=['hello'])
def greet(message):
    bot.reply_to(message, f'Привет @{message.from_user.username}! Как дела?')


@bot.message_handler(commands=['commands'])
def help(message):
    bot.send_message(message.chat.id, '`/commands - показывает весь список доступных команд\n`'
                                      '`/info - обо мне`\n'
                                      '`/hello - здоровается с написавшим`', parse_mode="MARKDOWN")


@bot.message_handler(commands=['info'])
def about(message):
    bot.send_message(message.chat.id, 'Привет. Меня зовут Минако Матсушима. Я студентка старшей школы. '
                                      'Я учу русский язык уже пять лет. Мои знания не очень большие, но '
                                      'у меня много русских и украинских друзей. Я хочу практиковаться и '
                                      'учиться больше. Давайте дружить!')


bot.polling()
