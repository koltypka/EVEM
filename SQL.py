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

    return  result

def getContent(WORD):
    if WORD:
        request = "SELECT * FROM INPUT_WORD WHERE WORD = '" + WORD + "'"
        SQLanswer = SQLQuery(request)
        return SQLanswer[0] if SQLanswer else []

# Функция возвращает динамический запрос на добавление элемента в базу данных
def insertQuery(WORD, NEWS_LIST):
    if WORD:
        INSERT = "INSERT INTO INPUT_WORD (WORD"
        VALUES = "VALUES ('" + WORD + "'"
        n = 1;
        for news in NEWS_LIST:
            if news:
                INSERT = INSERT + ", NEWS_" + str(n)
                VALUES = VALUES + ", '" + str(news) + "'"
            n = n + 1
        request = INSERT + ") " + VALUES + ");"
        return SQLQuery(request)

# Функция возвращает динамический запрос на добавление элемента в базу данных
def updateQuery(WORD, NEWS_LIST):
    if WORD:
        UPDATE = "UPDATE INPUT_WORD SET"
        #VALUES = "VALUES ('" + WORD + "'"
        n = 1;
        for news in NEWS_LIST:
            if news:
                if n > 1:
                    UPDATE = UPDATE + ','
                UPDATE = UPDATE + " NEWS_" + str(n) + " = " + "'" + str(news) + "'"
            n = n + 1
        request = UPDATE + "WHERE WORD = '" + WORD + "'"
        return SQLQuery(request)

#функция вызывается при запосе пользователя
def addRequest(WORD, NEWS_LIST):
    if WORD:
        newsList = getContent(WORD)
        counter = 0
        oldNewsList = []

        for i in range(5):
            if newsList['NEWS_' + i]:
                counter = counter + 1
                oldNewsList.append(newsList['NEWS_' + i])

        if NEWS_LIST.lenght < counter:
            newsLeftToAdd = counter - NEWS_LIST.lenght
            for oldNews in oldNewsList:
                if not newsLeftToAdd:
                    break
                NEWS_LIST.append(oldNews)
        else:
            return insertQuery(WORD, NEWS_LIST)

if __name__ == '__main__':
    #print(insertQuery('Новости сегодня', {'{ddddd}', '{3333}'}))  # dictionary
    #print(getContent('выы сегодня'))  # dictionary
    #print(updateQuery('Новости сегодня', {'{ddddd}', '{3333}'}))
