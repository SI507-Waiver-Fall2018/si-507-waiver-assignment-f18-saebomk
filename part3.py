# Saebom Kwon, saebom, 38120092, SI507 Waiver

import requests
from bs4 import BeautifulSoup

url = 'http://www.michigandaily.com'
g = requests.get(url)

soup = BeautifulSoup(g.content, 'html.parser')

def get_link(item):
    link_list = []
    li = soup.select("ol > li > a")
    for link in li:
        link_list.append(link.get('href'))
    return link_list

link_list = get_link(soup.find_all('ol'))

def article_info(item):
    toon_url = 'http://www.michigandaily.com' + item
    g = requests.get(toon_url)
    soup = BeautifulSoup(g.content, 'html.parser')
    title = soup.find('title')
    title = title.text.replace(" | The Michigan Daily", "")
    try:
        author = soup.select('.byline > .link > a')[0].text
    except:
        author = None
    return title, author

most_read_list = []

for link in link_list:
    most_read_data = (article_info(link))
    most_read_list.append(most_read_data)

print("Michigan Daily -- MOST READ")
for title, author in most_read_list:
    print(title, "\n  by", author)
