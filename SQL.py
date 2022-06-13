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
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

        cursorSaver = cursor
    finally:
        connection.close()

    return  cursorSaver

def getContent(keyWord, connection):
    #try:
        #with connection.cursor() as cursor:
            # SQL
            #sql = "SELECT Dept_No, Dept_Name FROM Department"
    return []

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
    print(insertQuery('ещё запрос', {'{ddddd}', '{3333}'}))  # dictionary