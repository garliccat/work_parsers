import requests
from bs4 import BeautifulSoup as bs
import random
import time
import csv
import os

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

def url_code(url):
    headers = {'User-Agent':random.choice(user_agent_list)}
    response = requests.get(url, headers=headers)
    return response.status_code

def get_html(url):
    try:
        headers = {'User-Agent':random.choice(user_agent_list)}
        r = requests.get(url, headers=headers)
    except:
        print('unable to reach page ' + url)
        return None
    return r.text

def write_csv(data):
    with open('pansionats.csv', mode='a', 
        newline='',
        encoding='utf-16'
        ) as f:
        #newline - to avoid blank rows after each record
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)

# write_csv(['title', 'description', 'facilities', \
#            'location', 'price', 'type', 'district', \
#            'inst_type', 'phone', 'meals', 'network', \
#            'mental_state', 'disease', 'phys_state', 'sex', \

def main():
    if os.path.isfile('pansionats.csv'):
        os.remove('pansionats.csv')
    add_header = True
    # os.mkdir('images')
    for pageindex in range(1, 32):
            
        url = f'https://top100pansionatov.ru/catalog/?page={pageindex}'
        print('\n', url, '\n', 'returns code: ', url_code(url), '\n')

        soup = bs(get_html(url), 'lxml')
        pans_cards = soup.find_all('a', {'class': 'btn more__info-btn'})

        for pan_card in pans_cards:
            print('\n')
            pan_url = 'https://top100pansionatov.ru' + pan_card['href']
            print('\n', pan_url, '\n', 'returns code: ', url_code(pan_url), '\n')

            pan_soup = bs(get_html(pan_url), 'lxml')

            inst_dict = {}

            try:
                inst_dict['Тайтл'] = pan_soup.find('h1', {'class': 'text-uppercase'}).get_text(strip=True)
            except:
                inst_dict['Тайтл'] = ''

            try:
                inst_dict['Дискрипшен'] = pan_soup.find('meta', {'name': 'description'})['content']
            except:
                inst_dict['Дискрипшен'] = ''

            try:
                inst_dict['Описание'] = pan_soup.find_all('div', \
                    {'class': 'ct-u-marginBottom20'})[4].get_text(strip=True)
            except:
                inst_dict['Описание'] = ''

            try:
                inst_dict['Удобства'] = ', '.join([i.get_text(strip=True) for i in pan_soup.find_all('span', {'class': 'text-capitalize_NO'})])
            except:
                inst_dict['Удобства'] = ''

            try:
                inst_dict['Адрес'] = pan_soup.find('h2', {'class': 'text-uppercase'}).get_text(strip=True)
            except:
                inst_dict['Адрес'] = ''

            try:
                inst_dict['Стоимость'] = pan_soup.find('span', {'class': 'ct-price'}).get_text(strip=True).replace('.', '')
            except:
                inst_dict['Стоимость'] = ''

            try:
                inst_dict['ЯКарты'] = 'https://yandex.ru/maps/?text=' + \
                    pan_soup.find('div', {'id': 'map'}).get('data-location').replace(', ', '%2C')
            except:
                inst_dict['ЯКарты'] = ''




            left_side_vals = ['Тип', 'Район', 'Тип учреждения', 'Круглосуточная  справочная', 'К-во питаний', \
                               'Сеть', 'Псих. состояние', 'Заболевание', 'Физ. систояние', 'Пол']

            for i in pan_soup.find_all('div', {'class': 'ct-u-displayTableRow'}):
                try:
                    value = i.find('span', {'class': 'ct-fw-600'}).get_text(strip=True)
                    if value in left_side_vals:
                        inst_dict[value] = i.find('div', {'class': 'ct-u-displayTableCell text-right'}).get_text(strip=True)
                except:
                    inst_dict[value] = ''

            for i in left_side_vals:
                if i not in inst_dict.keys():
                    print('MISSING: ', i)
                    inst_dict[i] = ''

            ### fetching images
            # folder_path = 'images/' + inst_dict['Тайтл'].replace('“', '')
            # if os.path.exists(folder_path):
            #     folder_path = folder_path + '_1'
            # os.mkdir(folder_path)
            # slides = pan_soup.find_all('img', {'class': 'img-responsive'})
            # for slide in slides:
            #     url = 'https://top100pansionatov.ru' + slide.get('src')
            #     r = requests.get(url, allow_redirects=True)
            #     open(folder_path + '/' + url.split('/')[-1], 'wb').write(r.content)

            for key in inst_dict.keys():
                print(key, ': ', inst_dict[key])
            print('\n\n')
               
            if add_header:
                write_csv(sorted(inst_dict.keys()))
                add_header = False
            write_csv([inst_dict[key] for key in sorted(inst_dict.keys())])

            inst_dict = {}


if __name__ == '__main__':
    main()
