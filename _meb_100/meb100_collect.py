import requests
from bs4 import BeautifulSoup as BS
import csv
import codecs
import re

''' collecting all the shit from meb100 pages '''

def get_html(url):
	try:
		r = requests.get(url)
	except:
		print('unable to reach site')
		return None

	return r.text

def get_data(html):
	if html == None:
		return None

	soup = BS(html, 'lxml')

	try:
		cards = soup.find_all('div', {'class':'factory organization-preview'})
		print('cards per page ' + str(len(cards)))
	except:
		print('unable to retrieve cards')
		return None # i donno about that !

	for card in cards:
		try:
			url = card.find('ul', {'id':'tabber__handles'}).find_all('li')[1].find('a').get('href')
		except:
			url = ''
			print('unable to retrieve url')
		full_url = 'https://www.meb100.ru' + url
		write_csv({'url':full_url})
		
	return {'url':url}

def write_csv(data):
	with open('meb100_parsed_urls.csv', 'a', newline='', encoding='utf-16') as f:
		#newline - to avoid blank rows after each record
		#encoding utf-16 - we are in russia, thats all
		writer = csv.writer(f)
		writer.writerow([data['url']])


def main():
	
	for i in range(1, 210):
			#print('page ' + str(i))
			url = 'https://www.meb100.ru/mebelnye-fabriki-opt?page={}'
			try:
				get_data(get_html(url.format(str(i))))
				print(url.format(str(i)))
				#write_csv(get_data(get_html('https://www.meb100.ru/mebelnye-fabriki-opt?page=' + str(i))))
				print('success')
			except:
				print('unable to retrieve site at all')
			print('\n')

		


if __name__ == '__main__':
	main()