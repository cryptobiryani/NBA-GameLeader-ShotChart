import nba_functions as nba
import create_shot_chart as csc
import csv
import pandas as pd
import twitter_upload_media
import credentials

if __name__ == '__main__':
    #Get path for image and CSV. CSV is used to store record of tweets posted to avoid repeats.
    image_file=credentials.image_file
    file_name=credentials.file_name
    today=nba.get_todays_games()
    game_codes=nba.get_game_code(today)
    for code in game_codes:
        #indicator variable is used for is_home(bool) variable. is_home = True --> home game, is home_false --> away game
        for indicator in [True, False]:
            game_date=nba.get_game_date(code)
            df=nba.get_scorer_df(today, code, indicator)
            if df is None:
                if indicator == True:
                    print(f"There is no home data for {code} yet.")
                else:
                    print(f"There is no away data for {code} yet.")
            else:
                game_records_df = pd.read_csv(file_name)
                df_code = game_records_df[game_records_df['game_code'] == code]
                if indicator in df_code.home.values:
                    print(f"This chart has already been posted.")
                else:
                    coords=nba.get_shot_coordinates(df)
                    csc.create_court(coords['x'], coords['y'], file_name=image_file, game_date=game_date, df=df)
                    game_date=nba.get_game_date(code)
                    tweet_text=f"{df['PLAYER_NAME'][0]} on {game_date} finished with {df['pts'][0]} points, {df['rebs'][0]} rebounds, and {df['ast'][0]} assists."
                    print(tweet_text)
                    twitter_upload_media.twitter_api().update_status_with_media(tweet_text, image_file)
                    with open(file_name, 'a') as csvfile: 
                        # creating a csv writer object 
                        csvwriter = csv.writer(csvfile, delimiter=',') 
                        rows=[[code, str(indicator)]]                         
                        # writing the data rows 
                        csvwriter.writerows(rows)
                                        
                



