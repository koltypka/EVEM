from fuzzywuzzy import fuzz
import rss
import SQL
import json
import yamlReader

def levenshtein_dist(a, b):
    def rec(i, j):
        if i == 0 or j == 0:
            return max(i, j)
        elif a[i - 1] == b[j - 1]:
            return rec(i - 1, j - 1)
        else:
            return 1 + min(
                rec(i, j - 1),
                rec(i - 1, j),
                rec(i - 1, j - 1)
            )
    return rec(len(a), len(b))

def fu1(word, news):
    word = word.lower()
    news = news.lower()
    lev_dist = levenshtein_dist(word, news)  # distance
    return ((len(s1) - lev_dist) / len(s1)) * 100  # ratio


def fu(word, news):
    word = word.lower()
    news = news.lower()
    return fuzz.partial_ratio(word, news)

def search_news_list(word, level=70):
    list_RSS = yamlReader.getYamlFile('RSS.yaml')
    result = []
    for url in list_RSS:
        if len(result) < 5:
            newsLits = search_news(word, url, level)
        else:
            break

        if newsLits:
            for news in newsLits:
                result.append(news)

    if len(result) < 5:
        try:
            bd_content = SQL.getContent(word)
            for i in range(1, 6):
                if bd_content['NEWS_'+str(i)] != '':
                    bd_news = json.loads(bd_content['NEWS_'+str(i)])
                    result.append(bd_news)
        except Exception as e:
            print("error search_news")
            print(e)

    L_add = []
    n = 5
    if len(result) < 5:
        n = len(result)
    for i in range(n):
        L_add.append(json.dumps(result[i], ensure_ascii=False))
    try:
        SQL.addRequest(word, L_add)
    except Exception as e:
        print("error search_news")
        print(e)

    return result


def search_news(word, url="https://tverigrad.ru/rss/rssfeed.php?ftype=all", level=70):
    L_news = []

    rss_content = rss.get_content(rss.supchik(url))

    for news in rss_content:
        t = fu(word, news['title'])
        d = fu(word, news['description'])
        if t > level or d > level:
            L_news.append(news)
    return L_news

if __name__ == '__main__':
    print(search_news_list("тверь"))