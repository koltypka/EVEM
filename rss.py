import requests
from bs4 import BeautifulSoup as BS
import json


def get_File_Data(FileName):  # возвращает текст файла
    with open(FileName, "r", encoding="utf-8") as f:
        return f.read()


def write_file_HTML(text, FileName="pupa.html"):  # запись в файл
    with open(FileName, "w", encoding="utf-8") as f:
        print(text, file=f)


def save_json_file(article_list, filename='news.json'):
    with open(filename, 'w', encoding="utf-8") as outfile:
        json.dump(article_list, outfile, ensure_ascii=False, indent=4)


def supchik():  # возвращает суп
    try:
        url = "https://tverigrad.ru/rss/rssfeed.php?ftype=all"
        source = requests.get(url)
        soup = BS(source.content, features="xml")
    except Exception as ex:
        print("ЖОПА supchik")
        print(ex)
    return soup


def get_content(soup=supchik()):  # словарь суп
    article_list = []
    try:
        articles = soup.findAll('item')
        for a in articles:
            title = a.find('title').text
            description = a.find('description').text
            link = a.find('link').text
            # guid = a.find('guid').text
            pubDate = a.find('pubDate').text
            # enclosure = a.find('enclosure').text

            article = {
                'title': title,
                'description': description,
                'link': link,

                'pubDate': pubDate

            }
            article_list.append(article)

        return article_list

    except Exception as e:
        print("ЖОПА get_content")
        print(e)


def get_content_one(soup=supchik()):
    aarticle_list = []
    try:
        aa = soup.find('item')

        title = aa.find('title').text
        description = aa.find('description').text
        link = aa.find('link').text
        # guid = a.find('guid').text
        pubDate = aa.find('pubDate').text
        # enclosure = aa.find('enclosure').text

        aarticle = {
            'title': title,
            'description': description,
            'link': link,

            'pubDate': pubDate

        }
        aarticle_list.append(aarticle)

        return aarticle_list

    except Exception as e:
        print("ЖОПА get_content_one")
        print(e)


if __name__ == '__main__':
    # s = supchik()
    #
    # print(s)  # xml
    # print()
    #
    # d = get_content(s)  # dictionary
    # print(d)
    print(get_content_one())  # dictionary
    # j = json.dumps(d, ensure_ascii=False, indent=4)  # json
    # print(j)
    #
    # dd = json.loads(j)  # dictionary from json
    # print(json.loads(j))
    #
    # save_json_file(d)
    # print(json.loads(get_File_Data("news.json")))  # dictionary from json file

