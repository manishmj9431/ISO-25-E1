from GoogleNews import GoogleNews

def getNews(query):
    googleNews = GoogleNews()
    googleNews.search(query)

    news = []

    i = 0

    number = min([len(googleNews.result()), 6])

    for result in googleNews.result():
        if (i > number):
            break
        
        n = {}
        n["title"] = result['title']
        n["description"] = result['desc']
        n["link"] = result['link']
    
        if (i == 0):
            n["image"] = result['img']
        news.append(n)

        i += 1

    googleNews.clear()

    return news




if __name__ == '__main__':
    query = input()
    print(getNews(query))