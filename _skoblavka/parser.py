
import codecs
import datetime
import csv
import os.path
from selenium import webdriver

date = datetime.date.today()

driver_path = r'C:\Users\Антон\Downloads\gecko\geckodriver.exe'

def main():
	driver = webdriver.Firefox(executable_path=driver_path)
	with codecs.open('urls.txt', 'r') as f:
		# global row
		for row in f:
			row = row.replace('\r\n', '')
			driver.get(row)
			catalog = driver.find_element_by_class_name('list-catalog')
			cards = catalog.find_elements_by_tag_name('li')
			for card in cards:
				try:
					description = card.find_element_by_tag_name('span').text
					print('Описание: ', description)
				except:
					description = ''
				
				try:
					art = card.find_elements_by_class_name('add_inf')[0].text.split('\nот ')[0].split('рт: ')[1]
					print('Артикул: ', art)
				except:
					art = ''

				try:
					price = card.find_element_by_tag_name('i').text.replace('от ', '')
					print('Цена: ', price)
				except:
					price = ''

				write_csv({'description':description, 'art':art, 'price':price, 'date':str(date)})
	driver.quit()

def write_csv(data):
	with open('skoblavka_parsed_data.csv', 'a', newline='', encoding='utf-16') as f:
		#newline - to avoid blank rows after each record
		#encoding utf-16 - we are in russia, thats all
		writer = csv.writer(f, delimiter=';')
		writer.writerow([data['art'], data['description'], data['price'], data['date']])

	# driver.stop_client

if __name__ == "__main__":
	if not os.path.isfile('skoblavka_parsed_data.csv'):
		write_csv({'art': 'art', 'description': 'description', 'price': 'price', 'date': 'date'})

	main()
