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

def getContent(keyWord):
    return [];

# Функция возвращает динамический запрос на добавление элемента в базу данных
def Dynamic_query(WORD, NEWS_1, NEWS_2, NEWS_3, NEWS_4, NEWS_5):
    requesting = "INSERT INTO INPUT_WORD (WORD, NEWS_1, NEWS_2, NEWS_3, NEWS_4, NEWS_5) VALUES ("
    reque = requesting +"'"+ WORD +"', " +"'"+ NEWS_1 +"', " +"'"+ NEWS_2+"', "+"'" + NEWS_3+"', "+"'"+ NEWS_4 +"', "+"'"+ NEWS_5 + ');'
    return reque