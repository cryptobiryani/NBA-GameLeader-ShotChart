import requests
import json
from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import shotchartdetail, boxscoretraditionalv2
import pandas as pd

import sys


f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 

def get_todays_games():
    '''
    Params: None
    Returns: Dictonary containing data on today's games
    '''
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()
    return games
def get_game_code(game_dict):
    '''Params: Dictionary 
       Return: List of game IDs 
    '''
    game_code_list=[]
    for game in game_dict:
        game_code_list.append(game['gameCode'])
    return game_code_list
def get_game_id(game_dict):
    game_id_list=[]
    for game in game_dict:
        if 'Final' in game['gameStatusText'] :
            game_id_list.append(game['gameId'])
    return game_id_list
def get_box_score(game_id):
    return boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_dict()  
def get_scorer_df(games_dict, game_code, is_home=True):
    '''
    Params: Dict of games, game code, boolean: if you want home team or away
    Return: Dataframe for a team's top scorer 
    '''
    if is_home == True:
        leader_index='homeLeaders'
        team_index='homeTeam'
    else:
        leader_index='awayLeaders'
        team_index='awayTeam'
    for game in games_dict:
        if 'Final' in game['gameStatusText'] and game['gameCode'] == game_code:
            scoring_leader=game['gameLeaders'][leader_index]['personId']
            team=game[team_index]['teamId']
            data=shotchartdetail.ShotChartDetail(player_id=scoring_leader, last_n_games=1, team_id=team, context_measure_simple = 'PTS').get_dict()['resultSets'][0]
            rows=data['rowSet']
            headers=data['headers']
            df=pd.DataFrame(rows)
            df.columns=headers
            df['pts']=game['gameLeaders'][leader_index]['points']
            df['ast']=game['gameLeaders'][leader_index]['assists']
            df['rebs']=game['gameLeaders'][leader_index]['rebounds']
            return df

def get_shot_coordinates(scorer_df):
    '''
    Params: Dataframe containing scorer with LOC_X and LOC_Y columns
    Returns: Dictionary with list values that contain x and y coordinates for each shot made
    '''
    return {'x':list(scorer_df['LOC_X']), 'y':list(scorer_df['LOC_Y'])}

def get_player_name(scorer_df):
    '''
    Params: Dataframe containing scorer with PLAYER_NAME column
    Returns: String containing player's full name
    '''
    return scorer_df['PLAYER_NAME'][0]

def get_team_acroynm(game_code, is_home=True):
    '''
    Params: Dataframe of scorer containing HTM and VTM columns, boolean indicating whether you want the home team or away team's acronym
    Returns: String containing the team's acronym
    '''
    if is_home == True:
            return game_code[9:12]
    #     return scorer_df['HTM'][0]
    elif is_home == False:
        return game_code[12:15]
    #     return scorer_df['VTM'][0]
    # elif is_home not in (True, False):
    #     print("is_home must be either True or False.")
    #     return None
def get_game_date(game_code):
    '''
    params: game code in this format --> 20230113/HOUSAC
    returns: date in mm/dd/yyy
    '''
    game_date_yyyymmdd=game_code.split('/')[0]
    game_date = datetime.strptime(game_date_yyyymmdd, '%Y%m%d').strftime('%m/%d/%Y')
    return game_date

