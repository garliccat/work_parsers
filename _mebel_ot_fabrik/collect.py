import requests
from bs4 import BeautifulSoup as BS
import csv
import codecs
import re

''' walking through all the urls from the list stored in fabrics.csv
and parsing all the data mentioned in get_data '''

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
		name = soup.find('div', {'class':'ms-sellerprofile description fon'}).find('h3').text.splitlines()[3]
	except:
		name = ''
		print('unable to retrieve name')

	try:
		description = soup.find('div', {'class':'seller-description'}).find('p').text
	except:
		description = ''
		print('unable to retrieve description')

	try:
		address = soup.find('li', {'class':'cont1'}).text
	except:
		address = ''
		print('unable to retrieve address')

	try:
		phone = soup.find('li', {'class':'cont2'}).text
	except:
		phone = ''
		print('unable to retrieve phone')

	#site = soup.find('div', {'class':'info-box'}).find('li', text = re.compile(r"(?<=Сайт: ).+(?=</li>)"), attrs = {'style':'display:none;'}).text
	try:
		site = soup.find(string=re.compile(r"(?<=Сайт: )(.*?)")).split()[1]
	except:
		site = ''
		print('unable to retrieve site address')

	return {'name':name, 'description':description, 'address':address, 'phone':phone, 'site':site}

def write_csv(data):
	with open('parsed.csv', 'a', newline='', encoding='utf-16') as f:
		#newline - to avoid blank rows after each record
		#encoding utf-16 - we are in russia, thats all
		writer = csv.writer(f, delimiter=';')
		writer.writerow([data['name'], data['address'], data['description'], data['phone'], data['site']])


def main():
	
	with codecs.open('fabrics.csv', 'rU', 'utf-16') as file:
		fieldnames = ['name', 'url']
		reader = csv.reader(file)

		for row in reader:
			print(row[1])
			#print(get_data(get_html(row[1])))
			try:
				write_csv(get_data(get_html(row[1])))
				print('success')
			except:
				print('unable to retrieve site at all')
			print('\n')

		


if __name__ == '__main__':
	main()