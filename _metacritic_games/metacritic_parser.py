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

def write_csv(data):
    with open('metacritic_games.csv', mode='a', newline='', encoding='utf-16') as f:
        #newline - to avoid blank rows after each record
        #encoding utf-16 - we are in russia, thats all
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)

write_csv(['title', 'platform', 'release_date', 'metascore', 'user_score', 'developer', 'rating', 'genres'])

num_lines = (sum(1 for line in open('urls.txt', 'r')))
step = 1
start_time = datetime.datetime.now()

with open('urls.txt', 'r') as urls:
    for url in urls:
        url = url.replace('\n', '')
        print('----\nStep {} from {} is {:0.3f}%'.format(step, num_lines, (step / num_lines * 100)))
        current_time = datetime.datetime.now()
        steps_left = num_lines - step
        time_left = ((current_time - start_time) / step) * steps_left
        print('Time left (approx.): ', time_left)

        try:
            soup = BS(get_html(url), 'lxml')

            try:
                title = soup.find('div', {'class': 'product_title'}).find('h1').get_text(strip=True)
                print('Title: ', title)
            except:
                title = ''
                print('Cant fetch title')

            try:
                platform = soup.find('span', {'class': 'platform'}).get_text(strip=True)
                print('Platform: ', platform)
            except:
                platform = ''
                print('Cant fetch platform')

            try:
                release_date = soup.find('li', {'class': 'summary_detail release_data'}).find_all('span')[1].get_text(strip=True)
                print('Release date: ', release_date)
            except:
                release_date = ''
                print('Cant fetch release date.')

            try:
                metascore = soup.find('div', {'class': 'metascore_wrap highlight_metascore'}).find('div', {'class': re.compile('^metascore_w .*')}).get_text(strip=True)
                print('Metascore: ', metascore)
            except:
                metascore = ''
                print('No metascore.')

            try:
                user_score = soup.find('div', {'class': re.compile('^metascore_w user.*')}).get_text(strip=True)
                if user_score == 'tbd':
                    user_score = ''
                    print('No userscore')
                print('Userscore: ', user_score)
            except:
                user_score = ''
                print('Cant fetch userscore')

            try:
                developer = soup.find('li', {'class': 'summary_detail developer'}).find_all('span')[1].get_text(strip=True)
                print('Developer: ', developer)
            except:
                developer = ''
                print('Cant fetch developer')

            try:
                rating = soup.find('li', {'class': 'summary_detail product_rating'}).find_all('span')[1].get_text(strip=True)
                print('Rating: ', rating)
            except:
                rating = ''
                print('Cant fetch rating')

            try:
                genres = soup.find('li', {'class': 'summary_detail product_genre'}).find_all('span', {'class': 'data'})
                genres_list = []
                for i in genres:
                    genres_list.append(i.get_text(strip=True))
                genres_list = '|'.join(genres_list)
                print('Genres: ', genres_list)
            except:
                genres_list = ''
                print('Cant fetch genres')

            write_csv([title, platform, release_date, metascore, user_score, developer, rating, genres_list])

        except:
            print('Cant get the URL: ', url)
            pass
        step += 1
        