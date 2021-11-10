from bs4 import BeautifulSoup
import requests

url = 'https://www.olx.ua/elektronika/noutbuki-i-aksesuary/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
items = soup.findAll('div', class_='offer-wrapper')

elements = []
try:
    for item in items:
        elements.append({
            'title': item.find('a', class_='marginright5 link linkWithHash detailsLink linkWithHashPromoted').get_text(strip=True),
            'price': item.find('p', class_='price').get_text(strip=True),
            'link': item.find('a', class_='marginright5 link linkWithHash detailsLink linkWithHashPromoted').get('href')
        })
        for element in elements:
            print(f'{element["title"]}\nЦена: {element["price"]}\nСсылка: {element["link"]}')
            print('=========' * 10)
except AttributeError:
    pass
 
