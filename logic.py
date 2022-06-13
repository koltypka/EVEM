from fuzzywuzzy import fuzz
import rss
import SQL
import json


def fu(word, news):
    word = word.lower()
    news = news.lower()
    return fuzz.partial_ratio(word, news)


def search_news(word, url="https://tverigrad.ru/rss/rssfeed.php?ftype=all", level=70):
    L_news = []

    rss_content = rss.get_content(rss.supchik(url))

    for news in rss_content:
        t = fu(word, news['title'])
        d = fu(word, news['description'])
        if t > level or d > level:
            L_news.append(news)


    if len(L_news) < 5:
        #try:
        bd_content = SQL.getContent(word)
        print(bd_content)
        for i in range(1, 6):
            if bd_content['NEWS_'+str(i)] != '':
                bd_news = json.loads(bd_content['NEWS_'+str(i)])
                L_news.append(bd_news)

        #except Exception as e:
            #print("error search_news")
            #print(e)


    L_add = []
    n = 5
    if len(L_news) < 5:
        n = len(L_news)
    for i in range(n):
        L_add.append(json.dumps(L_news[i], ensure_ascii=False))
    try:
        SQL.addRequest(word, L_add)
    except Exception as e:
        print("error search_news")
        print(e)
    return L_news


if __name__ == '__main__':
    print(search_news("вертолет"))