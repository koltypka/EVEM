import telebot
import SQL
import yamlReader
import logic

#получаем параметры из yaml файла
parametrs = yamlReader.getYamlFile('parameters.yaml')

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

    oldNewsList = logic.search_news_list(str(m.text.lower()))
    newsList = []
    if oldNewsList:
        for oldElem in oldNewsList:
            flag = True
            for newElem in newsList:
                if newElem['link'] == oldElem['link']:
                    flag = False
            if flag:
                EVEM.send_message(m.chat.id,
                                  oldElem['title'] + '\n\n' + oldElem['description'].replace('.>', '') + '\n\n' + oldElem['link'])
                newsList.append(oldElem)
    else:
        EVEM.send_message(m.chat.id, 'Не найдено')

# Запускаем бота
EVEM.polling(none_stop=True, interval=0)