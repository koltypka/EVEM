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
        return SQLQuery(request)

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
            n = n+1
        request = INSERT + ") " + VALUES + ");"
        return SQLQuery(request)

if __name__ == '__main__':
    #print(insertQuery('ещё запрос', {'{ddddd}', '{3333}'}))  # dictionary
    #print(getContent('дед'))  # dictionary