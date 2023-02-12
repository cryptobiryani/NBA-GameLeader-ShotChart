import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
import nba_functions as nba

# Plots court
def create_court(x,y,df, game_code, game_date,file_name, color='white'):
    '''
    Params: list of x coordinates, list of y coordinates,
            dataframe of team's top scorer, court color
    Return: Plot of basketball with made shots of top scorer plotted
    '''
    todays_date=datetime.today().strftime('%Y-%m-%d')
    fig = plt.figure(figsize=(4, 3.76))
    ax = fig.add_axes([0, 0, 1, 1])

    mpl.rcParams['font.family'] = 'Bodoni 72'
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['axes.linewidth'] = 2
    mpl.rcParams['text.color']="black"
    mpl.rcParams["font.weight"] = "bold"

    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    
    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    # Free Throw Arc
    ax.add_artist(mpl.patches.Arc((0, 190), 120, 118, angle=180, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2, ls='dashed'))
    ax.add_artist(mpl.patches.Arc((0, 190), 120, 118, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    # Inner Arc
    ax.add_artist(mpl.patches.Arc((0, 60), 85, 85, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 5, facecolor='none', edgecolor=color, lw=2))
    
    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('#E9B683') #DEB887
    
    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    
    y=[num+60 for num in y]
    x=[-1*num for num in x]
    ax.hexbin(x, y, gridsize=(50, 50), extent=(-300, 300, 0, 940), mincnt=1, alpha=.8, color='green', cmap='Greens', bins='log')
    ax.text(-240, 450, f"{nba.get_player_name(df)} ({df['pts'][0]}PTS, {df['ast'][0]}AST, {df['rebs'][0]}REBS) \n {nba.get_team_acroynm(game_code)} VS {nba.get_team_acroynm(game_code, is_home=False)} on {game_date}", ha='left', va='top')
    plt.savefig(file_name, dpi=300)
    plt.close(fig)
