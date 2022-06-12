from multiprocessing import connection
import pymysql
from soupsieve import select
import yamlReader
from config import host, user, password, db_name, port
Word1 = "sdg"
Newss_1 = "sgs"
Newss_2 = "2sshdf"
Newss_3 = "drfhrj"
Newss_4 = "tjns56"
Newss_5 = "ejlnjsr"
# Функция возвращает динамический запрос на добавление элемента в базу данных
def Dynamic_query(WORD, NEWS_1, NEWS_2, NEWS_3, NEWS_4, NEWS_5):
    requesting = "INSERT INTO INPUT_WORD (WORD, NEWS_1, NEWS_2, NEWS_3, NEWS_4, NEWS_5) VALUES ("
    reque = '"' + requesting +"'"+ WORD +"', " +"'"+ NEWS_1 +"', " +"'"+ NEWS_2+"', "+"'" + NEWS_3+"', "+"'"+ NEWS_4 +"', "+"'"+ NEWS_5 + ');'+ '"'
    return reque


try:
    # соединение
    connection = pymysql.connect(
        host = host,
        port = port,
        user = user,
        password = password,
        database = db_name,
        cursorclass = pymysql.cursors.DictCursor
    )
    print("Подключение успешно")
    print('#'*20)

    try:
        # добавляем ДИНАМИЧЕСКИ данные в таблицу
        def pushData():
            with connection.cursor() as cursor:
                    #INSERT INTO INPUT_WORD (WORD, NEWS_1, NEWS_2, NEWS_3, NEWS_4, NEWS_5) VALUES ('0','1','2','3','4','5');
                    #insert_query = Dynamic_query(Word1, Newss_1, Newss_2, Newss_3, Newss_4, Newss_5)
                    a = Dynamic_query(Word1, Newss_1, Newss_2, Newss_3, Newss_4, Newss_5)
                    print(a)
                    insert_query = a
                    print(insert_query)
                    cursor.execute(insert_query)
                    connection.commit()
        pushData()

    finally:
        connection.close()
        print("Все готово")

except Exception as ex:
    print("Ошибка подключения")
    print(ex)