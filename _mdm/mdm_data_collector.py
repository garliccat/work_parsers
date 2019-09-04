import requests
from bs4 import BeautifulSoup as BS
import csv
import codecs
import datetime

# urls for parsing are from the mdm_urls.csv
'''
cookies.txt file must consists of:
PHPSESSID WHATEVERVALUEYOUHAVE
'''

cookies = {}
f = open('cookies.txt', 'r')
f = f.read()
(key, val) = f.split()
cookies[key] = val


def get_html(url):
	try:
		r = requests.get(url, cookies=cookies)
	except:
		print('unable to reach page')
		return None

	return r.text


def get_data(html):
	if html == None:
		return None

	soup = BS(html, 'lxml')

	cards = len(soup.find_all('div', {'class':'cat-text'}))

	for i in range(0, cards):
		description = soup.find_all('div', {'class':'cat-name'})[i].get_text(strip=True)
		art = soup.find_all('div', {'class':'cat-info'})[i].get_text(strip=True)
		price_wholesale = soup.find_all('div', {'class':'cat-price'})[i].get_text(strip=True).split('руб.')[0].replace(' ', '').replace('.', ',')
		price_retail = soup.find_all('div', {'class':'cat-price-info'})[i].get_text(strip=True).split('руб.')[0].replace(' ', '').replace('.', ',')

		date = datetime.date.today()

		print({'art':art, 'description':description, 'price_retail':price_retail, 'price_wholesale':price_wholesale, 'date':str(date)})
		write_csv({'art':art, 'description':description, 'price_retail':price_retail, 'price_wholesale':price_wholesale, 'date':str(date)})

	

def write_csv(data):
	with open('mdm_collected_data.csv', 'a', newline='', encoding='utf-16') as f:
		#newline - to avoid blank rows after each record
		#encoding utf-16 - we are in russia, thats all
		writer = csv.writer(f, delimiter=';')
		writer.writerow([data['art'], data['description'], data['price_retail'], data['price_wholesale'], data['date']])




def main():
	
	with codecs.open('mdm_urls.csv', 'rU', 'utf-8') as file:
		#fieldnames = ['url']
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