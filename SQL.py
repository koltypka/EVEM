import pymysql.cursors
import yamlReader

# Функция возвращает connection.
def getConnection():
    parametrs = yamlReader.getYamlFile('SQL.yaml')

    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host=parametrs['host'],
                     user=parametrs['user'],
                     password=parametrs['password'],
                     db=parametrs['db'],
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
    return connection

#запрос в БД
def SQLQuery(query):
    connection = getConnection()
    result = []
    try:
        cursor = connection.cursor()
        cursor.execute(query)

        if query.split()[0] in ['INSERT', 'DELETE', 'UPDATE']:
            connection.commit()
            result.append('SUCCES')

        if query.split()[0] == 'SELECT':
            for row in cursor:
                result.append(row)
    finally:
        connection.close()

    return result

#получение элемента из БД по запросу
def getContent(WORD):
    if WORD:
        request = "SELECT * FROM INPUT_WORD WHERE WORD = '" + WORD + "'"
        SQLanswer = SQLQuery(request)
        return SQLanswer[0] if SQLanswer else []

# Функция возвращает динамический запрос на добавление элемента в БЛ
def insertQuery(WORD, NEWS_LIST):
    if WORD:
        INSERT = "INSERT INTO INPUT_WORD (WORD"
        VALUES = "VALUES ('" + WORD + "'"
        n = 1
        for news in NEWS_LIST:
            if news:
                INSERT = INSERT + ", NEWS_" + str(n)
                VALUES = VALUES + ", '" + str(news) + "'"
            n = n + 1
        request = INSERT + ") " + VALUES + ");"
        return SQLQuery(request)

# Функция возвращает динамический запрос на обновления свойств элемента в БД
def updateQuery(WORD, NEWS_LIST):
    if WORD:
        UPDATE = "UPDATE INPUT_WORD SET"
        n = 0
        for news in NEWS_LIST:
            n = n + 1

            if not news:
                continue
            if n > 1:
                UPDATE = UPDATE + ','

            UPDATE = UPDATE + " NEWS_" + str(n) + " = " + "'" + str(news) + "'"

        request = UPDATE + "WHERE WORD = '" + WORD + "'"
        return SQLQuery(request)

#функция вызывается при запросе пользователя
def addRequest(WORD, NEWS_LIST):
    if WORD:
        newsList = getContent(WORD)
        counter = 0
        oldNewsList = []

        if len(newsList) > 0:
            for i in range(5):
                if newsList['NEWS_' + str(i+1)]:
                    counter = counter + 1
                    oldNewsList.append(newsList['NEWS_' + str(i+1)])

            newsLeftToAdd = 5 - len(NEWS_LIST)
            for oldNews in oldNewsList:
                if newsLeftToAdd < 1:
                    break
                NEWS_LIST.append(oldNews)
                newsLeftToAdd = newsLeftToAdd - 1
            return updateQuery(WORD, NEWS_LIST)
        else:
            return insertQuery(WORD, NEWS_LIST)
