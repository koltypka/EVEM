import pymysql.cursors
import yaml
from yaml.loader import SafeLoader

# Функция возвращает connection.
def getConnection():
    with open('SQL.yaml') as f:
        parametrs = yaml.load(f, Loader=SafeLoader)
    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host=parametrs['host'],
                     user=parametrs['user'],
                     password=parametrs['password'],
                     db=parametrs['db'],
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
    return connection