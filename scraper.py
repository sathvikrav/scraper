# This program scrapes a webpage containing information on last year's premier league assist leaders

from bs4 import BeautifulSoup
from csv import writer
import pandas as pd
import requests
from geopy.geocoders import Nominatim
from sqlite import PremierDatabase
import folium
import requests_cache
import time

t_initial = time.process_time() # start the timer for program execution
requests_cache.install_cache() # cache the request to worldfootball to save time on future program executions
response = requests.get('https://www.worldfootball.net/assists/eng-premier-league-2019-2020/')
soup = BeautifulSoup(response.text, features="html.parser")
premier = PremierDatabase()
premier.create_table()

table = soup.find(name="table", attrs={"class": "standard_tabelle"}) # grab the table containing the player information
player_list = table.find_all("td") # we use the td table cell html tag since that is where each table row is located

with open("assists.csv", "w", encoding="utf-8") as csv_file: # open csv file to store player information
    csv_writer = writer(csv_file)
    headers = ['Name', 'Country', 'Team', 'Assists']
    csv_writer.writerow(headers)

    for option in player_list:
        if "player_summary" in str(option):
            player_name = option.get_text()
            if premier.select_player(player_name) == None:
                player_country = option.find_next_sibling("td").find_next_sibling("td").get_text() # get the next cell directly to the right in the table
                player_team = option.find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").contents[3].get_text()
                player_assists = option.find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find("b").get_text()
                csv_writer.writerow([player_name, player_country, player_team, player_assists])
                premier.insert_player(player_name, player_country, player_team, player_assists, 50.0, 50.0) # substitute dummy latitude and longitude into the database, will eventually be using geopy to get lat and long using country name and cache requests from geopy

print(premier.select_player("Kevin De Bruyne"))
premier.close() # close the database
time_final = time.process_time() - t_initial # end time for program execution
print("Program execution time was", time_final)