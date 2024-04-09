import requests
import pandas as pd
import psycopg2
from common import db_params, insert_f
import traceback
import logging
import time


ts = time.time()

### select films from db

def selected_films():
    # connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # select query
    query = "select title, year from films_top"
    cursor.execute(query)

    # save result into a variable
    films_from_db = cursor.fetchall()

    # close connection
    cursor.close()
    conn.close()

    return films_from_db

films_from_db = selected_films()

### retrieve films' details from api
api_url = 'http://www.omdbapi.com'
tags = ['Title', 'Year', 'Rated', 'Runtime', 'Genre', 'Director', 'Actors', 'Plot', 'Country', 'Awards', 'Poster', 'imdbRating', 'imdbVotes', 'BoxOffice']

# list to save data
films_details = []

# go through each film to retrieve details from api
for film in films_from_db:
    params = {
        'apikey' : 'd71c96a0',
        't' : film[0],
        'y' : str(film[1])
    }

    # try to connect to api
    try:
        response = requests.get(api_url, params=params)
        api_data = response.json()
        
        # if there is an error skip it
        if api_data.get('Response') == 'False':
            print(api_data.get('Error'))
            continue
        
        # needed details
        films_details.append(tuple(api_data.get(tag) for tag in tags))
    
    # log errors
    except Exception as e:
        logging.error(traceback.format_exc())

# load data to db
insert_f(films_details, 'films_data')

te = time.time()

print(te-ts)