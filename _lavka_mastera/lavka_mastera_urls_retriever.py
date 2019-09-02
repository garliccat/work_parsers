import requests
from bs4 import BeautifulSoup as BS
import csv
import codecs
import datetime
import re


root_url = 'https://xn----7sbabaiy0bgp0ckn.xn--p1ai'

def get_html(url):
	try:
		r = requests.get(url)
	except:
		print('unable to reach page ' + url)
		return None
	return r.text

def get_data(html):
	if html == None:
		return None

	try:
		soup = BS(html, 'lxml')
		print(soup.title.string)
		cards = soup.find_all('li', {'class':'b-product-groups-gallery__item'})
		print(f'stage 1 cards: {len(cards)}')
		for card in cards:
			
			try:
				soup_2 = BS(get_html(root_url + card.find('a', {'class':'b-product-groups-gallery__title'}).get('href')), 'lxml')
				cards_2 = soup_2.find_all('li', {'class':'b-product-groups-gallery__item'})
				print(f'stage 2 cards: {len(cards_2)}')
				for card_2 in cards_2:
					
					try:
						soup_3 = BS(get_html(root_url + card_2.find('a', {'class':'b-product-groups-gallery__title'}).get('href')), 'lxml')
						cards_3 = soup_3.find_all('li', {'class':'b-product-groups-gallery__item'})
						print(f'stage 3 cards: {len(cards_3)}')
						if len(cards_3) == 0:
							get_arts(get_html(root_url + card_2.find('a', {'class':'b-product-groups-gallery__title'}).get('href')))
						for card_3 in cards_3:
							get_arts(get_html(root_url + card_3.find('a', {'class':'b-product-groups-gallery__title'}).get('href')))

					except:
						print('exception on stage 3')
						get_arts(get_html(soup_2.find('a', {'class':'b-product-gallery__image-link'}).get('href')))
						return None

			except:
				print('exception on stage 2')
				get_arts(get_html(root_url + soup.find('a', {'class':'b-product-gallery__image-link'}).get('href')))
				return None

	except:
		get_arts(html)
		print('exception on stage 1')
		return None

def get_arts(html):
	print('get_arts call')
	soup = BS(html, 'lxml')
	cards = soup.find_all('li', {'data-qaid':'product-block'})
	print(f'cards in get_arts: {len(cards)}')
	for card in cards:
		url = card.find('a', {'class':'b-product-gallery__image-link'}).get('href')
		print('art URL is: ' + url)
		write_csv({'url':url})
	return None

def write_csv(data):
	with open('lavka_mastera_urls.csv', 'a', newline='', encoding='utf-16') as f:
		writer = csv.writer(f)
		writer.writerow(data['url'])


def main():
	print('Root URL: ' + root_url)
	get_data(get_html(root_url))
	return None	


if __name__ == '__main__':
	main()