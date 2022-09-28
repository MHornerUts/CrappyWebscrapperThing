# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from bs4 import BeautifulSoup
from operator import itemgetter
from csv import writer

import requests

url = input("GIVE ME URL ")
print("URL RECEIVED")


print("Doing shit!")

page = requests.get(url)

# print(page)

soup = BeautifulSoup(page.content, 'html.parser')
pagination = soup.find('div', class_="pagination")

total = 1

try:
    pages = pagination.find_all('a')

    for page in pages:
        a = page.text

        if a.isdigit():
            x = int(a)
            if x > total:
                total = x
except AttributeError:
    print("One page")

books = []
hrms = []


def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


session = requests.Session()


for spork in range(total):
    number = str(spork + 1)
    urlBig = url + "?page=" + number
    page = session.get(urlBig)
    soup = BeautifulSoup(page.content, 'html.parser')
    hrms.append(soup)
    print("PROCESSING page no " + number)


with open('List.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['Title', 'Rating', 'Score', 'Url', 'Number of Ratings']
    thewriter.writerow(header)
    for hrm in hrms:

        lists = hrm.find_all('tr', itemscope="")

        for list in lists:
            title = list.find('span', itemprop="name").text
            rating = list.find('span', class_="minirating").text.split()[0]
            score = str(list.find('a', href="#").text.split()[1])
            score = score.replace("of", "None")
            numberOfRatings = str(list.find('span', class_="minirating").text.split()[4])
            bookURL = list.find('a', class_="bookTitle")
            bookURL = "https://www.goodreads.com" + bookURL['href']

            if isFloat(rating):
                books.append([title, rating, score, bookURL, numberOfRatings])

    books.sort(key=itemgetter(1), reverse=True)
    for book in books:
        thewriter.writerow(book)

print("Done")