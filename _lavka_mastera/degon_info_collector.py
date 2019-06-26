import requests
from bs4 import BeautifulSoup as BS
import csv
import codecs
import datetime
import re

'''urls for parsing are taking from degon_urls.cvs
'''

def get_html(url):
	try:
		r = requests.get(url)
	except:
		print('unable to reach page')
		return None
	return r.text



def get_data(html):
	if html == None:
		return None

	soup = BS(html, 'lxml')

	try:
		category = soup.find('h1', {'class':'b-caption'}).get_text(strip=True)
	except:
		print('unable to locate category')
	#cards = soup.find('ul', {'class':'b-product-gallery'}).find_all('li', {'class':'b-online-edit b-product-gallery__item  js-rtb-partner'})
	try:
		cards = soup.find_all('li', {'data-qaid':'product-block'})
	except:
		print('cant fetch cards')

	print('cards on page: ' + str(len(cards)))

	for card in cards:
		art = card.find('span', {'class':'b-product-gallery__sku b-goods-sku'}).get_text(strip=True)
		#art = ''
		description = card.find('a', {'id':re.compile('link_to_product_')}).get_text(strip=True)
		#description = ''
		price = card.find('span', {'class':'b-goods-price__value b-goods-price__value_type_current'}).get_text(strip=True).split('руб')[0].replace(u'\xa0', u'')
		#price = ''
		url = card.find('a', {'class':'b-product-gallery__image-link'}).get('href')
		#url = ''
		date = datetime.date.today()

		print({'art':art, 'description':description, 'price':price, 'url':url, 'category':category, 'date':str(date)})
		write_csv({'art':art, 'description':description, 'price':price, 'url':url, 'category':category, 'date':str(date)})

	

def write_csv(data):
	with open('degon_parsed_data.csv', 'a', newline='', encoding='utf-16') as f:
		#newline - to avoid blank rows after each record
		#encoding utf-16 - we are in russia, thats all
		writer = csv.writer(f, delimiter=';')
		writer.writerow([data['art'], data['description'], data['category'], data['price'], data['url'], data['date']])




def main():
	
	with codecs.open('degon_urls.csv', 'rU', 'utf-8') as file:
		reader = csv.reader(file)

		for row in reader:
			print(row[0])
			try:
				#print(get_data(get_html(row[0])))
				#write_csv(get_data(get_html(row[0])))
				get_data(get_html(row[0]))
				print('success, something was recieved')
			except:
				print('error, something went wrong, cant fetch info')
			print('\n')


if __name__ == '__main__':
	main()