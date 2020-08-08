from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as BS
import csv
import codecs
import datetime
import re


def get_html(url):
    try:
        r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    except:
        print('unable to reach page ' + url)
        return None
    return urlopen(r)

def get_data(html):
    if html == None:
        return None

    try:
        soup = BS(html, 'lxml')
        pages = soup.find('li', {'class': 'page last_page'}).find('a', {'class': 'page_num'}).get_text(strip=True)
        print(f'pages with games: {pages}')
        for page in range(int(pages)):
            try:
                print(root_url + str(page))
                url = root_url + str(page)
                soup_2 = BS(get_html(url), 'lxml')

                for game in soup_2.find_all('li', {'class': re.compile('^product game_product.*')}):
                    url = 'https://www.metacritic.com' + game.find('div', {'class': 'basic_stat product_title'}).find('a').get('href')
                    # name = game.find('div', {'class': 'basic_stat product_title'}).get_text(strip=True)
                    # print(name, ' - ', url)
                    # print(url)
                    to_file(url)

                print('DONE')

            except:
                print(f'exception on page {page}')
                return None

    except:
        print('could not get the pages numbers')
        return None


def to_file(data):
    with open('urls.txt', 'a') as f:
        f.write(data + '\n')



def main():
    platforms = ['xboxone', 'ps4', 'pc']
    global root_url
    for platform in platforms:
        root_url = 'https://www.metacritic.com/browse/games/release-date/available/{}/date?page='.format(platform)
        print('Platform: ', platform.upper())
        # print('Root URL: ' + root_url)
        get_data(get_html(root_url + '0'))
    return None


if __name__ == '__main__':
    main()