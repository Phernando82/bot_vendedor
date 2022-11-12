import telebot
import csv
from decouple import config

token_bot = config('TOKEN_BOT')
# instanciar o bot
bot = telebot.TeleBot(token_bot)

notificados = []

with open('pago_chat_ids.csv', 'r', encoding='utf8') as csvfile:
    e = csv.reader(csvfile)
    for usuario in e:
        user_id = usuario[0]
        if user_id not in notificados:
            notificados.append(user_id)
            bot.send_message(user_id, 'Estamos com uma super promoção')
