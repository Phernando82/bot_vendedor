import csv
import telebot
from decouple import config
from telebot.types import LabeledPrice
from datetime import datetime

token_bot = config('TOKEN_BOT')
token_stripe = config('TOKEN_STRIPE')

precos = [
    LabeledPrice(label='Mensal', amount=1000),
]
# instanciar o bot
bot = telebot.TeleBot(token_bot)

respostas = {
    'oi': 'Olá! Em que posso ajudar?',
    'bom dia': 'Bom dia! Em que posso ajudar?',
    'boa tarde': 'Boa tarde, em que posso ajudar?',
    'boa noite': 'Boa noite, em que posso ajudar?',
    'boa noite': 'Boa noite, em que posso ajudar?',
    'qual é o preco?': 'O preço é de R$ 10,00',
    'qual é o preço': 'O preço é de R$ 10,00',
    'qual o preço': 'O preço é de R$ 10,00',
    'qual o preço?': 'O preço é de R$ 10,00'
}


# função salvar os chat ids
def salvar_id(arquivo_destino, dados: list):
    with open(arquivo_destino, 'a', newline='', encoding='utf8') as csvfile:
        e = csv.writer(csvfile)
        e.writerow(dados)


# funções de comando
@bot.message_handler(commands=['start', 'inicio'])
def start(message):
    salvar_id('chat_ids.csv', [message.from_user.id])
    bot.send_message(message.chat.id,
                     'Olá! Tudo bem?\n Este é um bot vendedor modelo \n Deseja comprar acesso ao canal? \n Clique em '
                     '\n /comprar \n Se deja mais informações clique em \n /ajuda'
                     )


@bot.message_handler(commands=['help', 'ajuda'])
def help(message):
    bot.send_message(message.chat.id, 'Você pode utilizar os seguintes comandos: \n '
                                      '/start para iniciar \n'
                                      '/comprar para comprar\n'
                                      '\n'
                                      'Perguntas frequentes:\n'
                                      'Quanto tempo para receber acesso após o pagamento?\n'
                                      'Após o pagamento o acesso é imediato\n'
                                      'Quais cartões são aceitos?\n'
                                      'Todos os cartões'
                     )


@bot.message_handler(commands=['comprar'])
def comprar(message):
    bot.send_invoice(
        message.from_user.id,
        title='Planos',
        description='Está disponível o plano mensal',
        provider_token=token_stripe,
        currency='BRL',
        photo_url=config('PHOTO_CHANNEL'),
        photo_height=512,
        photo_width=512,
        photo_size=512,
        is_flexible=False,
        prices=precos,
        invoice_payload='PAYLOAD'
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True, error_message='Alguém tentou roubar os dados do seu cartão,\
              mas protegemos com sucesso suas credenciais, tente pagar novamente em alguns minutos.'
    )


@bot.message_handler(content_types=['successful_payment'])
def pagou(message):
    salvar_id('pago_chat_ids.csv', [message.from_user.id, datetime.now().strftime('%d/%m/%Y %H:%M')])
    bot.send_message(message.from_user.id, 'Obrigado pela compra! Seu acesso foi liberado')


@bot.message_handler(commands=['download'])
def download(message):
    doc = open('teste.pdf', 'rb')
    bot.send_document(message.chat.id, doc)


@bot.message_handler(func=lambda m: True)
def tudo(message):
    print('Mensagem: ', message.text)
    texto = message.text
    salvar_id('historico_chat_ids.csv', [message.from_user.id, message.text, datetime.now().strftime('%d/%m/%Y %H:%M')])
    resp = respostas.get(str(message.text).lower(), 'Não entendi. Tente novamente ou use o comando /ajuda')
    bot.send_message(message.from_user.id, resp)


# startar o bot
bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
