import pandas as pd
import requests
from bs4 import BeautifulSoup


# Obtenir les pages
pages = [str(i) for i in range(1,11)]
url = "https://www.scrapethissite.com/pages/forms/?page={}"
response = requests.get(url.format("1"))
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')

# Obtenir les noms des colonnes sinon il stocke les années dans les buts et c'est foireux
header = [th.text.strip() for th in table.find_all('th')]

# Initialiser un DataFrame vide pour stocker les données scrapées
results_df = pd.DataFrame(columns=header)

# Parcourir les pages et extraire les données
for page in pages:
    # Requête HTTP GET sur l'url de la page
    response = requests.get(url.format(page))
    # Parsing du contenu HTML de la page
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    for row in rows:
        values = [td.text.strip() for td in row.find_all('td')]
        if int(values[8]) > 0 and int(values[7]) < 300 :
            #A remplacer si possible par la méthode concat de pandas pour eviter les warnings, mais on a pas trouvé comment, déso Rida ne nous tape pas dessus stp
            results_df = results_df.append(pd.Series(values, index=header), ignore_index=True)

# Supprimer les doublons, parce que les doublons c'est brouillon
#results_df.drop_duplicates(subset=['Team Name'], inplace=True)

# Trier les données
results_df.sort_values(['+ / -'], ascending=False, inplace=True)

# Écrire les résultats le fichier csv
results_df.to_csv('results.csv', index=False)