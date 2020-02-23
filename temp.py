from GoogleNews import GoogleNews

def getNews(query):
    googleNews = GoogleNews()
    googleNews.search(query)

    news = []
    for result in googleNews.result():
        n = {}
        n["title"] = result['title']
        n["description"] = result['desc']
        n["link"] = result['link']

        news.append(n)

    googleNews.clear()

    return news

if __name__ == '__main__':
    query = input()
    print(getNews(query))