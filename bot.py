# оставь надежду всяк сюда входящий


import telebot

bot = telebot.TeleBot('')  # sorry :P


@bot.message_handler(commands=['hello'])
def greet(message):
    bot.reply_to(message, 'Привет Как дела?')


bot.polling()
