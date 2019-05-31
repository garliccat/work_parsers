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
		name = soup.find('div', {'class':'col-xs-12 col-sm-8 col-md-10 description-organization'}).find('h1').get_text(strip=True)
	except:
		name = ''
		print('unable to retrieve name')

	# parsing content blocks which could be with phones only, or with address
	try:
		info_blocks = soup.find_all('div', {'class':'content-line'})
		if len(info_blocks) > 1:
			site = soup.find_all('div', {'class':'content-line'})[0].find('a').get_text(strip=True)
			phones = soup.find_all('div', {'class':'content-line'})[1].find_all('span', {'style':'display: inline-block; padding-right: 16px;'})
			phone = ''
			for i in phones:
				phone+=(i.get_text(strip=True)[1:] + ' , ')
		else:
			phones = soup.find('div', {'class':'content-line'}).find_all('span', {'style':'display: inline-block; padding-right: 16px;'})
			phone = ''
			for i in phones:
				phone+=(i.get_text(strip=True)[1:] + ' , ')
			site = ''
	except:
		site = ''
		phone = ''
		print('couldnt resolve site or phone')

	try:
		description = soup.find('div', {'class':'col-xs-8 col-md-6 shot-description'}).get_text(strip=True)
	except:
		description = ''
		print('unable to retrieve description')

	# parsing bottom block for boss contacts
	try:
		bottom_boxes = soup.find_all('div', {'class':'col-xs-12 col-sm-6 col-md-4'})
		if len(bottom_boxes) > 1:
			if soup.find_all('div', {'class':'col-xs-12 col-sm-6 col-md-4'})[0].get_text(strip=True).split(":")[0] == 'Руководитель':
				boss = soup.find_all('div', {'class':'col-xs-12 col-sm-6 col-md-4'})[0].get_text(strip=True).split(":")[1]
		else:
			boss = ''
	except:
		boss = ''
		print('unable to retrieve boss info')

	try:
		address = soup.find_all('div', {'id':'content__address'})[1].get_text(strip=True)
		try:
			city = address.split(' ')[1].split(',')[0]
		except:
			city = ''

	except:
		address = ''
		print('unable to retrieve address')


	return {'name':name, 'city':city, 'address':address, 'site':site, 'description':description, 'phones':phone, 'boss':boss}

	


def write_csv(data):
	with open('meb100_parsed_info.csv', 'a', newline='', encoding='utf-16') as f:
		#newline - to avoid blank rows after each record
		#encoding utf-16 - we are in russia, thats all
		writer = csv.writer(f, delimiter=';')
		writer.writerow([data['name'], data['city'], data['address'], data['site'], data['phones'], data['description'], data['boss']])




def main():
	
	with codecs.open('meb100_parsed_urls.csv', 'rU', 'utf-16') as file:
		#fieldnames = ['url']
		reader = csv.reader(file)

		for row in reader:
			print(row[0])
			try:
				#print(get_data(get_html(row[0])))
				write_csv(get_data(get_html(row[0])))
				print('success, something was recieved')
			except:
				print('error, something went wrong, cant fetch info')
			print('\n')




if __name__ == '__main__':
	main()