import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.scrapethissite.com/pages/simple/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    countries = soup.find_all('div', class_='country')

    csvfile = open('datacountry.csv', mode='w', newline='', encoding='utf-8')
    fieldnames = ['name', 'capital', 'population', 'surface']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for country in countries:
        name = country.find('h3', class_='country-name').text.strip()
        capital = country.find('span', class_='country-capital').text.strip()
        population = country.find('span', class_='country-population').text.strip()
        surface = country.find('span', class_='country-area').text.strip()

        writer.writerow({
            'name': name,
            'capital': capital,
            'population': population,
            'surface': surface
        })

    csvfile.close()

    csv_filename = 'datacountry.csv'
    with open(csv_filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print(f"Contenu du fichier {csv_filename} :")
        print()
        for row in reader:
            print(f"Name: {row['name']}, Capital: {row['capital']}, Population: {row['population']}, Surface: {row['surface']}")