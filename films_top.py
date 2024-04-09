from bs4 import BeautifulSoup
import requests
import re
import psycopg2
from common import db_params, insert_f
import time 

ts = time.time()

# prepare to parse 
url = 'https://www.cinemarealm.com/best-of-cinema/empires-500-greatest-movies-of-all-time/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# focus on content
entry_content = str(soup.find('div', class_ = 'entry-content'))

# extract film names and years
pattern = '\<strong\>(.*)\<\/strong\>.*(\d\d\d\d)\)'
extracted = re.findall(pattern, entry_content)

# load data into db
insert_f(extracted, 'films_top')

te = time.time()

print(te-ts)
