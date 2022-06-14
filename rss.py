import requests
from bs4 import BeautifulSoup as BS
import json
import SQL
import yamlReader

def get_File_Data(FileName):  # возвращает текст файла
    with open(FileName, "r", encoding="utf-8") as f:
        return f.read()

def write_file_HTML(text, FileName="pupa.html"):  # запись в файл
    with open(FileName, "w", encoding="utf-8") as f:
        print(text, file=f)

def save_json_file(article_list, filename='news.json'):
    with open(filename, 'w', encoding="utf-8") as outfile:
        json.dump(article_list, outfile, ensure_ascii=False, indent=4)

def supchik(url):  # возвращает суп
    try:
        url = url
        source = requests.get(url)
        soup = BS(source.content, features="xml")
    except Exception as ex:
        print("ошибка supchik")
        print(ex)
    return soup

#получает все новости
def get_content(soup):  # словарь суп
    article_list = []
    try:
        articles = soup.findAll('item')
        for a in articles:
            title = a.find('title').text
            description = a.find('description').text
            link = a.find('link').text
            pubDate = a.find('pubDate').text

            article = {
                'title': title,
                'description': description,
                'link': link,
                'pubDate': pubDate
            }
            article_list.append(article)

        return article_list

    except Exception as e:
        print("ошибка get_content")
        print(e)


# получает на вход суп
def get_content_one(soup):
    aarticle_list = []
    try:
        aa = soup.find('item')

        title = aa.find('title').text
        description = aa.find('description').text
        link = aa.find('link').text
        pubDate = aa.find('pubDate').text

        aarticle = {
            'title': title,
            'description': description,
            'link': link,
            'pubDate': pubDate
        }
        aarticle_list.append(aarticle)

        return aarticle_list

    except Exception as e:
        print("ошибка get_content_one")
        print(e)

def get_all_rss_news(key_word):
    aarticle_list = SQL.getContent(key_word)
    if  len(aarticle_list) < 5:
        list_RSS = yamlReader.getYamlFile('RSS.yaml')
        for RSS_link in list_RSS:
            aarticle_list.append(
                get_content(
                    supchik(RSS_link)))

            if len(aarticle_list) > 5:
                break
    return aarticle_list
