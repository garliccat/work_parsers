import requests
from bs4 import BeautifulSoup as BS

def get_html(url):
	r = requests.get(url)
	return r.text

def get_data(html):
	soup = BS(html, 'lxml')
	h1 = soup.find('div', {'id':'content'}).find('li', {'class':'cont2'}).text
	return h1


def main():
	url = 'http://mebelotfabrik.ru/sellers/allant'
	print(get_data(get_html(url)))


if __name__ == '__main__':
	main()