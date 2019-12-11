import requests
from requests import get
from bs4 import BeautifulSoup
import sqlite3
import json
from secret_data import OMDb_API_Key
import csv
import sys
# import plotly
# import plotly.express as px

# Caching imdb json
IMDB_CACHE_FNAME = 'cache_imdb.json'
try:
    cache_file = open(IMDB_CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    IMDB_CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    IMDB_CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_imdb_cache(url, header):
    unique_ident = get_unique_key(url)

    if unique_ident in IMDB_CACHE_DICTION:
        # print("Getting cached data...")
        return IMDB_CACHE_DICTION[unique_ident]

    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, headers=header)
        IMDB_CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(IMDB_CACHE_DICTION)
        fw = open(IMDB_CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return IMDB_CACHE_DICTION[unique_ident]


# Caching OMDB json
OMDB_CACHE_FNAME = 'cache_omdb.json'
try:
    cache_file = open(OMDB_CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    OMDB_CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    OMDB_CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_" + "_".join(res)

def make_request_using_OMDB_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in OMDB_CACHE_DICTION:
        # print("Fetching cached data...")
        return OMDB_CACHE_DICTION[unique_ident]

    else:
        # print("Making a request for new data...")
        resp = requests.get(baseurl, params)
        # print(resp.url)
        OMDB_CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(OMDB_CACHE_DICTION)
        fw = open(OMDB_CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return OMDB_CACHE_DICTION[unique_ident]
#cache end

# Function
# 1.Guess:
# a.Input 5 movie names and guess which one has the highest rating and highest box office. (e.g., A user types in Avatar, Iron Lady, Iron Man, Toy Story 3, Moonlight as 5 movies, and guesses that Avatar has the highest box office while Moonlight has the best review.)
# b.Reveal the answer and provide the URL of the movie poster.
# c.Open a new website page which displays a histogram graph and bubble chart.
# d.Create a new CSV file with the table contains production companies.
#
# 2.2018 Top 100 Movies:
# Open a new website page displays the pie chart with the top 100 movies.
#

def get_imdb_data(page):
    imdb_database = {}
    # for single_page in range(1):
    url = page
    # + "&page=" + str(single_page)
        # print(page_url)
    header = {'User-Agent': 'SI_CLASS'}
    page_text = make_request_using_imdb_cache(url, header)
    page_soup = BeautifulSoup(page_text, 'html.parser')
        # params = {"name": name, "title":title}
        # return make_request_using_cache(catalog_url, params)
        # print(page_text)

    # content_div = page_soup.find_all('div',class_="lister-item-content")
    content_div = page_soup.select("h3 > a")

    for movie_name in content_div:
        # print(movie_name)
        name = movie_name.text
        movie_url_end = movie_name["href"]
        one_movie_url = imdb_baseurl + movie_url_end
        imdb_id = movie_url_end[7:16]
        # print(name)
        # print(box_office_url)
        movie_text = make_request_using_imdb_cache(one_movie_url, header)
        movie_soup = BeautifulSoup(movie_text, 'html.parser')
        movie_rating_all = movie_soup.find_all('div', class_='ratingValue')
        movie_story = movie_soup.find_all('div', id='titleStoryLine')
        # movie_page = movie_soup.find_all('div', class_="article",id='titleDetails')
        # movie_box_office = movie_soup.find_all('Cumulative Worldwide Gross:')
        # print(movie_box_office)
        # print(movie_page)
        for one_rating in movie_rating_all:
            rating = one_rating.find('span').text

        for one_story in movie_story:
            story_line_sec = one_story.find('div',class_="inline canwrap")
            storyline = story_line_sec.find('span').text
            # print(storyline)

        ### add to imdb_database
            imdb_database[name] = {}
            imdb_database[name]["name"] = name
            imdb_database[name]["rating"] = rating
            imdb_database[name]["stroyline"] = storyline
            imdb_database[name]["imdb_id"] = imdb_id


    #### Write out imdb file here #####
    dumped_output_json = json.dumps(imdb_database)
    output_file = open('imdb_dict.json', 'w')
    output_file.write(dumped_output_json)
    output_file.close()

#### Execute funciton, get_imdb_data,here ####
imdb_baseurl = 'https://www.imdb.com/'
directory_url = imdb_baseurl + '/best-of/top-100-movies-of-2018/ls047677021/'

get_imdb_data(directory_url)



#### Execute funciton, get OMBD data by using imdb_id derived from json ####

imdb_file = open('imdb_dict.json', 'r')
cache_imdb_contents = imdb_file.read()
CACHE_IMDB_DICTION = json.loads(cache_imdb_contents)
imdb_file.close()


def get_OMDB_data(dic):
    ids_lst = []
    # imdb_dic = {}
    imdb_dic_lst = []
    for imdb_movie in CACHE_IMDB_DICTION:
        # movie_Name = CACHE_IMDB_DICTION[imdb_movie]['name']
        imdb_ID = CACHE_IMDB_DICTION[imdb_movie]['imdb_id']
        # print(imdb_ID)
        ids_lst.append(imdb_ID)
    # print(ids_lst)
        # imdb_dic[movie_Name] = {}
        # # imdb_dic[movie_Name]["movie_Name"] = movie_Name
        # imdb_dic[movie_Name]['imdb_ID'] = imdb_ID
        # # imdb_database[imdb_ID] = imdb_ID
    # print(imdb_dic)
    for one_movie_id in ids_lst:
        # print(one_movie_id)
        OMDB_url = 'http://www.omdbapi.com/?'
        # apikey='+ OMDb_API_Key + '&i='+ str(imdb_dic[movie_Name]['imdb_ID'])
        params = {
        "apikey": OMDb_API_Key
        }
        params["i"] = one_movie_id
        resp = make_request_using_OMDB_cache(OMDB_url, params)
        # imdb_dic['Title'] = resp['Title']
        # imdb_dic['Ratings'] = resp['Ratings']
        # imdb_dic['BoxOffice'] = resp['BoxOffice']
        # imdb_dic['Poster'] = resp['Poster']
        imdb_dic_lst.append(resp)

    # return imdb_dic_lst

    #### Write out OMDB file here #####
    dumped_output_json = json.dumps(imdb_dic_lst)
    output_file = open('omdb_dict.json', 'w')
    output_file.write(dumped_output_json)
    output_file.close()



get_OMDB_data(CACHE_IMDB_DICTION)


# 3.Help:
# Tell users how to play with this program.
#
# 4.Exit:
# End the program.
