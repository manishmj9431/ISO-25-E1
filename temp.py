from GoogleNews import GoogleNews
import requests

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

def getBooks(name):
    r = requests.get("http://openlibrary.org/search.json", {'q': name})
    data = r.json()
    docs = data['docs']

    num = min(data['num_found'], 2)

    books = []

    i = 0
    for doc in docs:
        if (i >= num):
            break

        book = {}
        book['title'] = doc['title']
        book['publisher'] = doc['publisher']
        book['authors'] = doc['author_name'] 
        books.append(book)
        i += 1

    return books

if __name__ == '__main__':
    query = input()
    print(getBooks(query))