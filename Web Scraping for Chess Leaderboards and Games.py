
import pandas as pd
import numpy as np

import time 
from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
import requests

# %% Scrape Player Usernames from Leaderboards

#Initialise chrome driver and list to store player usernames
driver = webdriver.Chrome()
usernames = []

#Loop through 3 major leaderboards - Bullet, Blitz and Rapid
for s in ["", "/bullet" , "/rapid"]:
    url = "https://www.chess.com/leaderboard/live" + s
    driver.get(url)
    time.sleep(5) #allow 5 seconds for page to load
    soup = bs4.BeautifulSoup(driver.page_source, 'html') #extract html from page - note leaderboards use javascript and hence selenium is required
    usernames += soup.find_all('a' , class_ = 'user-username-component user-username-blue-with-dark-mode user-username-link user-tagline-username' ) # add all usernames found in each leaderboard
    
#Create Pandas series and clean data ; removing duplicates and any white space 
usernames = pd.Series(usernames)
usernames = usernames.apply(lambda x: x.text.strip())
usernames.drop_duplicates(inplace=True)



# %% Scrape Games Data

#Initialise numpy array to store games data
col_names = ['Username (White)' ,   'Rating (White)' , 'Title (White)' , 'Username (Black)', 'Rating (Black)', 'Title (Black)' 
             ,'Result' , 'Accuracy', 'Moves Count' , 'Date' , 'Time Control' , 'Tournament Game']
games = np.array(col_names)

#Select number of pages to iterate through for each player - note each page contains a maximum of 50 games
max_pages = 4

#Begin Scraping Games Data
for user in usernames:
    n = 1
    print(user)
    while n <= max_pages:
        try:        
            #Create URL and get HTML
            url = 'https://www.chess.com/games/archive/' + user + '?gameOwner=other_game&gameType=live&gameTypeslive%5B%5D=rapid&gameTypeslive%5B%5D=blitz&gameTypeslive%5B%5D=bullet&timeSort=desc&page='  + str(n) ;
            page = requests.get(url)
            time.sleep(15)
            soup = BeautifulSoup(page.text, 'html')
        
            #Begin Web Scraping
            tr_all = soup.find_all('tr')[1:] # get HTML for each row
            for tr in tr_all:
                row = []

                #Player data
                #Iterate through each player and append data to 'row'
                player_data = tr.find_all('div', class_ = 'archive-games-user-tagline')
                for player in player_data:
                    title = player.find('a', class_ = 'post-view-meta-title')
                    name = player.find('a', class_ = 'user-username-component user-username-blue-with-dark-mode user-tagline-username')
                    rating = player.find('span', class_ = 'user-tagline-rating')
                    
                    #Add player data to 'row'
                    #Note Title may be empty if player does not have a fide title
                    name = name.text.replace('\n', '').strip()
                    rating = rating.text.replace('\n', '').strip()
                    row += [name , rating ]
                    
                    if title != None: 
                        title = title.text.replace('\n', '').strip()
                        row += [title]
                    else:
                        row += [None]

                #Find and Clean remaining Features and Add to row
                # Result
                result_white = tr.find_all('div' , class_ = 'archive-games-result-wrapper-score')
                result_white = [data.text.replace('\n', '').strip() for data in result_white ]
                # Player Accuracy
                player_accuracy = tr.find('td' , class_ = 'table-text-center archive-games-analyze-cell')
                player_accuracy = player_accuracy.text.replace('\n' , ' ').strip()
                #Moves
                move_count = tr.find('td' , class_ = 'table-text-center archive-games-analyze-cell').next_sibling.next_sibling
                move_count = move_count.text.replace('\n' , ' ' ).strip()
                # Date
                date = tr.find_all('td' , class_ = 'table-text-right archive-games-date-cell')
                date = [data.text.replace('\n', '').strip() for data in date ]
                # Time Control
                game_type = tr.find('span', class_ = 'archive-games-game-time')
                game_type = game_type.text.replace('\n', '').strip()
                #Tournament Game
                #Note tournaments can take two forms: order and arena: applying find_all to both and adding will return a list which, if not empty, will signify if this is a tournament game
                tournament_game = tr.find_all('span', class_ = 'icon-font-chess archive-games-additional-icon arena') + tr.find_all('span', class_ = 'icon-font-chess archive-games-additional-icon order')
                if (tournament_game == []): 
                    tournament_game = 'N' 
                else: 
                    tournament_game = 'Y'

                #Add to rows 
                row += [result_white.pop() , player_accuracy , move_count , date.pop() , game_type , tournament_game ]
                #Add row data to games_data dataframe
                games = np.vstack([games , row])
            n += 1
                
        except:
            #Throw exception in case of error and continue scraping
            print("Error with user  ", user ," Page " , n)
            n += 1

#Create Pandas Dataframe from data
games = pd.DataFrame( games[1:,] , columns= col_names )

