import telebot
import yaml
import SQL
from yaml.loader import SafeLoader

#получаем параметры из yaml файла
with open('parameters.yaml') as f:
    parametrs = yaml.load(f, Loader=SafeLoader)

connection = SQL.getConnection()

# Создаем экземпляр бота
EVEM = telebot.TeleBot(parametrs['token'])

# Функция, обрабатывающая команду /start
@EVEM.message_handler(commands=["start"])
def start(m, res=False):
    EVEM.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')

# Функция, обрабатывающая команду /bad
@EVEM.message_handler(commands=["bad"])
def bad(m, res=False):
    if m.chat.id in parametrs['TestIds']:
        EVEM.send_message(m.chat.id, 'ответ плохой, исправляюсь(')

# Функция, обрабатывающая команду /ok
@EVEM.message_handler(commands=["ok"])
def ok(m, res=False):
    if m.chat.id in parametrs['TestIds']:
        EVEM.send_message(m.chat.id, 'ответ принят, стараюсь в том же духе!')

# Функция, обрабатывающая команду /myId
@EVEM.message_handler(commands=["myId"])
def myId(m, res=False):
    if parametrs['idCheck']:
        EVEM.send_message(m.chat.id, 'Ваш ID: ' + str(m.chat.id))

# Получение сообщений от юзера
@EVEM.message_handler(content_types=["text"])
def handle_text(m):
    if m.chat.id in parametrs['TestIds']:
        EVEM.send_message(m.chat.id, 'вы админ')
    else:
        #тут будет отправка полученого сообщения в БД
        EVEM.send_message(m.chat.id, 'Вы написали:')

    for text in m.text.lower().split():
        EVEM.send_message(m.chat.id, text)

# Запускаем бота
EVEM.polling(none_stop=True, interval=0)