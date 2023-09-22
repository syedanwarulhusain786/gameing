
import random
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from IPython.display import Image, display
from difflib import SequenceMatcher

import pandas as pd


# load csv file into a dataframe

def get_player_photo_url(player_id):
    # print(abadan01)
    print(player_id)
    
    url = f'https://www.baseball-reference.com/players/{player_id[0]}/{player_id}.shtml'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img = soup.find('div', {'class': 'media-item'}).find('img')
    if img is not None:
        return img['src']
    else:
        return None

def play_game(combined_data_filtered, level):
    if level == 'easy':
        players = combined_data_filtered[(combined_data_filtered['AB'] >= 500) & (combined_data_filtered['yearID.x'] >= 1975) & (combined_data_filtered.groupby('playerID.x')['yearID.x'].transform('count') >= 7)]
    elif level == 'medium':
        players = combined_data_filtered[(combined_data_filtered['AB'] >= 500) & (combined_data_filtered['yearID.x'] >= 1975) & ((combined_data_filtered.groupby('playerID.x')['yearID.x'].transform('count') >= 4) & (combined_data_filtered.groupby('playerID.x')['yearID.x'].transform('count') < 7))]
    elif level == 'hard':
        players = combined_data_filtered[(combined_data_filtered['AB'] >= 500) & (combined_data_filtered['yearID.x'] >= 1975) & ((combined_data_filtered.groupby('playerID.x')['yearID.x'].transform('count') >= 2) & (combined_data_filtered.groupby('playerID.x')['yearID.x'].transform('count') < 4))]
    elif level == 'difficult':
        players = combined_data_filtered[(combined_data_filtered['AB'] >= 500) & (combined_data_filtered['yearID.x'] >= 1975)]
    else:
        print("Invalid level selected")
        return None, None, None

    # Select a random player from the filtered data frame
    player_index = random.randint(0, len(players) - 1)
    player_id = players.iloc[player_index]['playerID.x']

    # Extract all years for the selected player
    player_years = combined_data_filtered[combined_data_filtered['playerID.x'] == player_id]

    player_years.rename(columns={"Position.1": "Position", "yearID.x": "Year"}, inplace=True)

    # Extract all columns except Fullname and playerID
    relevant_stats = [col for col in player_years.columns if col not in ["Fullname", "playerID.x", "playerID.y", "yearID.y", "combined", "stint", "playerID", "yearID", "most_common_position", "first_season", "combined11"]]

    player_stats = player_years[relevant_stats].reset_index(drop=True)
    player_name = player_years.iloc[0]['Fullname']

    return player_stats, player_name, player_id

def start(level,combined_data_filtered):

    # Define a variable to keep track of the player's score
    score = 0

    # Define a variable to keep track of the player's score for close guesses
    close_guess_score = 0.5
    # Example usage of function
    # Initialize score to 0
    score = 0

    player_stats, player_name, player_id = play_game(combined_data_filtered, level)
    print("Based on the following statistics, can you guess the player?")
    print(player_stats.to_string(index=False))
    guess = input("Guess the player: ")

    # Calculate name similarity score between guess and actual player name
    name_similarity = SequenceMatcher(None, guess.lower(), player_name.lower()).ratio()
    if guess.lower() == player_name.lower():
        player_photo_url = get_player_photo_url(player_id)
        if player_photo_url is not None:
            display(Image(url=player_photo_url))
        print("Congratulations! You got it right.")
        # Increment score by 1 and display current score
        score += 1
        print(f"Current score: {score}")
    elif name_similarity >= 0.8:
        player_photo_url = get_player_photo_url(player_id)
        print(f"Close enough! The player was {player_name}.")
        if player_photo_url is not None:
            display(Image(url=player_photo_url))
        # Increment score by close_guess_score and display current score
        score += close_guess_score
        print(f"Current score: {score}")
    else:
        print(f"Sorry, that's incorrect. The correct answer was {player_name}.")
        player_photo_url = get_player_photo_url(player_id)
        if player_photo_url is not None:
            display(Image(url=player_photo_url))
    # display current score
        print(f"Current score: {score}")



    # play_again_input = input("Do you want to play again? (yes/no) ")
    # while play_again_input.lower() not in ["yes", "no"]:
    #     play_again_input = input("Invalid input. Do you want to play again? (yes/no) ")

    # play_again = (play_again_input.lower() == "yes")


