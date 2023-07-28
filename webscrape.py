import csv
import requests
from bs4 import BeautifulSoup

def extract_record(item):
    atag = item.find('h2')
    if atag and atag.a:
        title = atag.a.text.strip()
        url = 'https://www.amazon.in' + atag.a['href']
    else:
        return None

    try:
        price_parent = item.find('span', class_='a-price')
        price = price_parent.find('span', class_='a-offscreen').text
    except AttributeError:
        price = ''

    try:
        rating = item.i.text
    except AttributeError:
        rating = ''

    try:
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        review_count = ''

    print("Title:", title)
    print("Price:", price)
    print("Rating:", rating)
    print("Review Count:", review_count)
    print("URL:", url)

    return title, price, rating, review_count, url

def main(search):
    records = []
    r = requests.get(f'https://www.amazon.in/s?k={search}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1')
    soup = BeautifulSoup(r.content, 'html.parser')

    results = soup.find_all('div', {'class': 'sg-col-inner'})
    if not results:
        print("No search results found.")
        return

    for item in results:
        record = extract_record(item)
        if record:
            records.append(record)

    with open('Python_Assignment.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'price', 'stars', 'review_count', 'url'])
        writer.writerows(records)

if __name__ == '__main__':
    main('bags')
