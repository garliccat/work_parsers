import requests
from bs4 import BeautifulSoup as BS
import csv


def get_html(url):
	r = requests.get(url)
	return r.text

def write_csv(data):
	with open('fabrics.csv', 'a', newline='', encoding='utf-16') as f:
		#newline - to avoid blank rows after each record
		#encoding utf-16 - we are in russia, thats all
		writer = csv.writer(f)
		writer.writerow([data['name'], data['url']])


def get_data(html):
	soup = BS(html, 'lxml')
	#table_of_cards = soup.find_all('div', {'class':'row'})[3]
	cards = soup.find_all('div', {'class':'product-layout product-list col-xs-12'})
	
	print(f'Total cards {len(cards)}')

	for card in cards:
		name = card.find('h4').text
		url = card.find('h4').find('a').get('href')

		data = {'name':name, 'url':url}
		#print(data)
		write_csv(data)


def main():
	#url = 'http://mebelotfabrik.ru/sellers//sellers/?limit=1063'
	#print(get_data(get_html(url)))



if __name__ == '__main__':
	main()