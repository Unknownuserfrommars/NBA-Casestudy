
# NBA Casestudy Python File
# Version 7.3
# Github Released

# Imports
import streamlit as st # type: ignore
from streamlit_option_menu import option_menu as menu # type: ignore
st.set_page_config(layout="wide")
import numpy as np  # type: ignore # noqa: E402
import plotly.express as px  # type: ignore # noqa: E402
import pandas as pd  # type: ignore # noqa: E402
pcq = px.colors.qualitative
pd.options.plotting.backend = "plotly"

my_path = ""

# Read in the dataset
player_totals = pd.read_csv(my_path + "Player Totals.csv")

# Player position cleaning
position_dict = {"SG":"G",
                "SF":"F",
                "PF":"F",
                "PG":"G",
                "C":"C",
                "SF-PF":"F",
                "SF-SG":"F-G",
                "SG-PG":"G",
                 "PF-SF":"F",
                "SG-SF":"F-G",
                "PF-C":"C-F",
                "PG-SG":"G",
                "C-PF":"C-F",
                "SG-PG-SF":"F-G",
                "SF-C":"C-F",
                "SG-PF":"F-G",
                "PG-SF":"F-G",
                "C-SF":"C-F",
                "SF-PG":"F-G",
                "G":"G",
                "F":"F",
                "C-F":"C-F",
                "F-C":"C-F",
                "F-G":"F-G",
                "G-F":"F-G"}

player_totals["ancient_pos"] = player_totals["pos"].map(position_dict)

# Creating a `seasons_played` column
player_totals_sort_values = player_totals.sort_values(by=['player_id', 'season']).head(50)[["season", 'player', 'experience']]
player_totals_drop_dups = player_totals_sort_values.drop_duplicates(subset=['player', 'season'])
player_totals_drop_dups_sorted = player_totals_drop_dups.sort_values(by=['player', 'season'])
player_totals_drop_dups_sorted['exp'] = player_totals_drop_dups_sorted.groupby('player').cumcount() + 1
player_totals_simplified = pd.merge(player_totals_sort_values, player_totals_drop_dups_sorted[['player', 'season', 'exp']], on=['player', 'season'], how='left')
player_totals['seasons_played'] = "Season " + player_totals['experience'].astype(str)

# Create the column for field goal misses and free throw misses (`fgm` and `ftm` respectively)
player_totals["fgm"] = player_totals["fga"] - player_totals["fg"]
player_totals["ftm"] = player_totals["fta"] - player_totals["ft"]

# Create the overall rating of a player in one season, used in later GOAT discussion
player_totals["ovr"] = player_totals["pts"] + player_totals["ast"] - player_totals["fgm"]*0.5 - player_totals["ftm"]*0.75

# Create a Player Efficiency Rating (PER) and similar composite stats
player_totals['per'] = (player_totals['pts'] + player_totals['ast'] + player_totals['trb'] + player_totals['stl'] + player_totals['blk'] - player_totals['ftm'] - player_totals['fgm']) / player_totals['g']
player_totals['ppg'] = player_totals['pts'] / player_totals['g']
player_totals['rpg'] = player_totals['trb'] / player_totals['g']
player_totals['orpg'] = player_totals['orb'] / player_totals['g']
player_totals['drpg'] = player_totals['drb'] / player_totals['g']
player_totals['apg'] = player_totals['ast'] / player_totals['g']
player_totals['bpg'] = player_totals['blk'] / player_totals['g']
player_totals['spg'] = player_totals['stl'] / player_totals['g']
player_totals['tpg'] = player_totals['tov'] / player_totals['g']

# Drop some columns that are not useful in this project
CVar = ["player","ancient_pos","lg","tm", "seasons_played"]
NVar = ['season',"experience","pts","ast","fg","fga","ft","fta","g", 'fgm', 'ftm', 'ovr', 'age', 'x3p', 'x3pa', 'x2p', 'x2pa', 'pf', 'tov', 'per', 'ppg', 'rpg', 'orpg', 'drpg', 'apg', 'bpg', 'spg']
nba_graph = player_totals[CVar + NVar].copy()

# Team name cleaning
team_dict = {"WSC":"WSC",
             "TRH":"TRH",
             "STB":"STB",
             "PRO":"PRO",
             'PIT':'PIT',
             "PHW":"GSW",
             'SFW':'GSW',
             'GSW':'GSW',
             'NYK':'NYK',
             'DTF':'DTF',
             'CLR':'CLR',
             'CHS':'CHS',
             'BOS':'BOS',
             'BLB':'BLB',
             'ROC':'SAC',
             'CIN':'SAC',
             'KCO':'SAC',
             'KCK':'SAC',
             'SAC':'SAC',
             'MNL':'LAL',
             'LAL':'LAL',
             'INJ':'INJ',
             'FTW':'DET',
             'DET':'DET',
             'WAT':'WAT',
             'TRI':'ATL',
             'MLH':'ATL',
             'STL':'ATL',
             'ATL':'ATL',
             'SYR':'PHI',
             'PHI':'PHI',
             'SHE':'SHE',
             'INO':'INO',
             'DNN':'DNN',
             'AND':'AND',
             'CHP':'WAS',
             'CHZ':'WAS',
             'BAL':'WAS',
             'CAP':'WAS',
             'WSB':'WAS',
             'WAS':'WAS',
             'CHI':'CHI',
             'SEA':'OKC',
             'OKC':'OKC',
             'SDR':'HOU',
             'HOU':'HOU',
             'PTP':'PTC',
             'MNP':'PTC',
             'PTC':'PTC',
             'OAK':'VIR',
             'WSA':'VIR',
             'VIR':'VIR',
             'NOB':'MMS',
             'MMP':'MMS',
             'MMT':'MMS',
             'MMS':'MMS',
             'NJA':'BRK',
             'NYA':'BRK',
             'NJN':'BRK',
             'BRK':'BRK',
             'MNM':'FLO',
             'MMF':'FLO',
             'FLO':'FLO',
             'KEN':'KEN',
             'IND':'INA',
             'INA':'INA',
             'HSM':'SSL',
             'CAR':'SSL',
             'SSL':'SSL',
             'DNR':'DEN',
             'DEN':'DEN',
             'DLC':'SAS',
             'TEX':'SAS',
             'SAA':'SAS',
             'SAS':'SAS',
             'ANA':'UTS',
             'LAS':'UTS',
             'UTS':'UTS',
             'PHO':'PHO',
             'MIL':'MIL',
             'POR':'POR',
             'CLE':'CLE',
             'BUF':'LAC',
             'SDC':'LAC',
             'LAC':'LAC',
             'SDA':'SDS',
             'NOJ':'UTA',
             'UTA':'UTA',
             'DAL':'DAL',
             'MIA':'MIA',
             'CHH':'CHO',
             'CHA':'CHO',
             'CHO':'CHO',
             'ORL':'ORL',
             'MIN':'MIN',
             'VAN':'MEM',
             'MEM':'MEM',
             'TOR':'TOR',
             'NOH':'NOP',
             'NOK':'NOP',
             'NOP':'NOP',
             'TOT':'Traded'}
nba_graph['present_teams'] = player_totals['tm'].map(team_dict)

# Define a `agg` function to aggregate data (will be used to aggregate data in later exploratory graphs)
def agg(data_frame: pd.DataFrame, groupby_cols: list | str = None, mode: str = 'sum') -> pd.DataFrame:
    """
    Parameters:
    data_frame (`pd.DataFrame`)
    groupby_cols (`list` of `str` or `str`): The columns to pd.groupby(). (If nothing entered, default columns will be 'player' and 'ancient_pos')
    mode (`str`): Accepts 'sum' or 'mean'

    Returns:
    `pd.DataFrame`
    """
    assert mode in ['sum', 'mean'], "`mode` must be one of 'sum' or 'mean'"
    cols = groupby_cols if groupby_cols is not None else ['player', 'ancient_pos']
    nvar = np.setdiff1d(NVar, cols)
    # print(cols)
    m = data_frame.copy()
    if mode == 'sum':
        return m.groupby(cols)[nvar].sum().reset_index()
    elif mode == 'mean':
        return m.groupby(cols)[nvar].mean().reset_index()

# Dictionaries
num_dict = {
    'season': 'Season',
    'experience': 'Years of Experience',
    'pts': 'Points',
    'ast': 'Assists',
    'fg': 'Field Goals',
    'fga': 'Field Goals Attempts',
    'ft': 'Free Throws',
    'fta': 'Free Throw Attempts',
    'g': 'Games Played',
    'fgm': 'Field Goals Missed',
    'ftm': 'Free Throws Missed',
    'ovr': 'Overall Score', # TODO: Same as line 242
    'x3p': '3 Pointers',
    'x3pa': '3 Pointers Attempted',
    'x2p': '2 Pointers',
    'x2pa': '2 Pointers Attempted',
    'pf': 'Personal Fouls',
    'tov': "Turnovers",
    'per': 'Player Efficiency Rating'
}
cat_dict = {
    'player': 'Player Name',
    'ancient_pos': 'Position', # TODO: Same as line 242
    'lg': 'League',
    'tm': 'Team',
    'seasons_played': 'Player Experience',
    'present_teams': 'Current Team Name' # TODO: Explain this in the description
}
team_dict = {
    'GSW': 'Golden State Warriors',
    'NYK':"New York Knicks",
    'BOS':'Boston Celtics',
    'SAC':'Sacramento Kings',
    'LAL':'Los Angeles Lakers',
    'DET':'Detroit Pistons',
    'ATL':"Atlanta Hawks",
    'PHI':"Philadelphia 76ers",
    'WAS':"Washington Wizards",
    'CHI':'Chicago Bulls',
    'OKC':"Oklahoma City Thunder",
    'HOU':"Houston Rockets",
    'BRK':"Brooklyn Nets",
    "DEN":"Denver Nuggets (Modern)",
    'SAA':"San Antonio Spurs",
    'PHO':'Phoenix Suns',
    'MIL':"Milwaukee Bucks",
    'POR':'Portland Trail Blazers',
    'CLE':"Cleveland Cavaliers",
    'LAC':"Los Angeles Clippers",
    'UTA':"Utah Jazz",
    'DAL':"Dallas Mavericks",
    'MIA':"Miami Heat",
    'CHO':'Charlotte Hornets',
    'ORL':"Orlando Magic",
    'MIN':'Minnesota Timberwolves',
    'MEM':'Memphis Grizzlies',
    "TOR":'Toronto Raptors',
    'NOP':"New Orleans Pelicans"
}
nba_graph['ptn'] = nba_graph['present_teams'].map(team_dict)
pos_dict = {
    "G":"Guard",
    "F":"Forward",
    "C":"Center",
    "C-F":"Center-Forward",
    'F-G':'Forward-Guard'
}
nba_75 = [
    "Kareem Abdul-Jabbar",
    "Ray Allen",
    "Giannis Antetokounmpo",
    "Carmelo Anthony",
    "Nate Archibald",
    "Paul Arizin",
    "Charles Barkley",
    "Rick Barry",
    "Elgin Baylor",
    "Dave Bing",
    "Larry Bird",
    "Kobe Bryant",
    "Wilt Chamberlain",
    "Bob Cousy",
    "Dave Cowens",
    "Billy Cunningham",
    "Stephen Curry",
    "Anthony Davis",
    "Dave DeBusschere",
    "Clyde Drexler",
    "Tim Duncan",
    "Kevin Durant",
    "Julius Erving",
    "Patrick Ewing",
    "Walt Frazier",
    "Kevin Garnett",
    "George Gervin",
    "Hal Greer",
    "James Harden",
    "John Havlicek",
    "Elvin Hayes",
    "Allen Iverson",
    "LeBron James",
    "Magic Johnson",
    "Sam Jones",
    "Michael Jordan",
    "Jason Kidd",
    "Kawhi Leonard",
    "Damian Lillard",
    "Jerry Lucas",
    "Karl Malone",
    "Moses Malone",
    "Pete Maravich",
    "Bob McAdoo",
    "Kevin McHale",
    "George Mikan",
    "Reggie Miller",
    "Earl Monroe",
    "Steve Nash",
    "Dirk Nowitzki",
    "Hakeem Olajuwon",
    "Shaquille O'Neal",
    "Robert Parish",
    "Chris Paul",
    "Gary Payton",
    "Bob Pettit",
    "Paul Pierce",
    "Scottie Pippen",
    "Willis Reed",
    "Oscar Robertson",
    "David Robinson",
    "Dennis Rodman",
    "Bill Russell",
    "Dolph Schayes",
    "Bill Sharman",
    "John Stockton",
    "Isiah Thomas",
    "Nate Thurmond",
    "Wes Unseld",
    "Dwyane Wade",
    "Bill Walton",
    "Jerry West",
    "Russell Westbrook",
    "Lenny Wilkens",
    "Dominique Wilkins",
    "James Worthy"
]

all_dict = num_dict.copy()
all_dict.update(cat_dict)

# No more cleaning code after this line!
# We will begin to code the things you will be seeing on the browser
with st.sidebar:
    s = menu(
        menu_title = 'The Great Navigation Pane of All Time',
        options = ['Abstract', 'Background Information', 'Data Cleaning','Finding the GOAT Player', 'Analysis for some of the Greatest Teams of All Time', 'Analysis of GOAT by stats for the ten most popular players', 'Analysis of the NBA Championship teams in iconic seasons', 'Rivalry Team Comparison', 'Conclusion', 'Bibliography'],
        menu_icon = 'house-door-fill',
        icons = ['person-arms-up', 'basket', 'filetype-csv', 'search', 'microsoft-teams', 'key-fill', 'trophy-fill', 'flag', 'star-fill', 'list-ol'],
        default_index = 0,
        )

if s == "Abstract":
    st.title("NBA GOAT Decision")
    st.markdown("The debate over who holds the title of the Greatest of All Time (GOAT) in the NBA is one of the most spirited conversations among basketball enthusiasts. From legendary feats to iconic moments, various factors contribute to the greatness of players. However, when the chatter clears and emotions settle, it's the cold, hard stats that offer an objective lens through which we can attempt to settle this debate.")
    st.markdown("In this case study, we delve deep into the world of numbers to crown the NBA GOAT.<sup>2,3,4</sup> We'll explore an array of statistical categories, including scoring averages, assists, rebounds, and advanced metrics. By examining these figures, we aim to provide a comprehensive analysis that transcends personal bias and nostalgia.", unsafe_allow_html=True)
    st.markdown("Join us as we crunch the numbers, compare legends from different eras, and unveil who truly stands atop the NBA mountain based on their statistical dominance. Whether you're a fan of the flashy dunks, the clutch shots, or the all-around game, this case study promises to offer insights and revelations about the legends of the hardwood. Let's dive in and find out who the stats say is the ultimate GOAT!")
    st.markdown("This dataset is retrieved from Kaggle (https://www.kaggle.com/) <sup>1</sup>", unsafe_allow_html=True)
    st.text("If you find and any bugs (or graphs not working as expected), please start a new ISSUE at the github repository.")

if s == "Background Information":
    st.title("Background Info")
    st.markdown("The quest to identify the NBA's Greatest of All Time (GOAT) has spanned decades, encompassing a multitude of eras, playing styles, and basketball philosophies. This ongoing debate has seen fans, analysts, and players themselves weigh in with passionate arguments in favor of various legendary figures.<sup>5</sup>", unsafe_allow_html=True)
    st.subheader("Key Contenders")
    st.markdown("<b>Michael Jordan</b>", unsafe_allow_html=True)
    st.markdown("Widely regarded as the pinnacle of basketball greatness, Michael Jordan's six championships with the Chicago Bulls, coupled with five MVP awards and ten scoring titles, make him a perennial favorite in GOAT discussions. His fierce competitiveness, iconic moments, and ability to elevate his game in the clutch have solidified his legacy.")
    st.markdown("<b>LeBron James</b>", unsafe_allow_html=True)
    st.markdown("LeBron James, with his extraordinary blend of size, skill, and basketball IQ, has consistently dominated the league since his debut. With multiple championships, MVP awards, and a near-unmatched ability to impact every aspect of the game, LeBron's case as the GOAT is bolstered by his longevity and versatility.")
    st.markdown("<b>Kareem Abdul-Jabbar</b>", unsafe_allow_html=True)
    st.markdown("Kareem Abdul-Jabbar's career is marked by his (ex) all-time leading scoring record, six MVP awards, and six championships. His signature skyhook shot remains one of the most unstoppable moves in basketball history, and his consistency over two decades highlights his enduring greatness.")
    st.markdown("<b>Magic Johnson and Larry Bird</b>", unsafe_allow_html=True)
    st.markdown("Magic Johnson and Larry Bird revitalized the NBA in the 1980s with their legendary rivalry. Magic's unparalleled vision and passing prowess, alongside Bird's sharpshooting and competitive fire, each earned them multiple championships and MVP awards, securing their places among the all-time greats.")
    st.markdown("<b>Wilt Chamberlain and Bill Russell</b>", unsafe_allow_html=True)
    st.markdown("Wilt Chamberlain's jaw-dropping statistics, including his 100-point game and the 50 PPG season, stand as monumental achievements. Conversely, Bill Russell's unparalleled success, with 11 championships in 13 seasons, underscores his impact on winning and defense.")
    st.markdown("<b>Stats Criteria</b>", unsafe_allow_html=True)
    st.markdown("To navigate the complexities of the GOAT debate, we will employ a range of statistical measures:")
    st.markdown("""
                - Scoring: Points per game (`PPG`), total points, and scoring titles.
                - Assists: Assists per game (`APG`), total assists, and assist titles.
                - Rebounds: Rebounds per game (`RPG`), total rebounds, and rebounding titles.
                - Advanced Metrics: An `ovr` (overall) score for each season based on the player's performances.
    """)
    st.markdown("<b>Context and Evolution of the Game</b>", unsafe_allow_html=True)
    st.markdown("""
                It's crucial to consider the context and evolution of the game when comparing players across different eras. Changes in rules, playing style, athleticism, and competition level can significantly impact statistical outputs. For instance, the pace of the game, three-point shooting prevalence, and defensive strategies have evolved, making direct comparisons challenging but necessary for a fair assessment.

                By grounding our analysis in these comprehensive statistics and contextual insights, we aim to shed light on who truly deserves the title of the NBA's Greatest of All Time.
    """)

# Data Cleaning
if s == "Data Cleaning":
    st.title("Data Cleaning")
    st.markdown("""
                <b>In this part, we are going to:</b>
                - Read in the data
                - Do some cleaning
    """, unsafe_allow_html=True)

    st.markdown("<b>Import the Dataset</b>", unsafe_allow_html=True)
    code1 = 'my_path=\'\'\nplayer_totals = pd.read_csv(f"{my_path}\\Player Totals.csv")'
    st.code(code1)

    st.markdown("<b>After inspection, the unique positions were too much. So i spent 1 hr fixing it</b>", unsafe_allow_html=True)
    code2 = 'position_dict = {"SG": "G", "SF": "F", "PF": "F", "PG": "G", "C": "C", "SF-PF": "F", "SF-SG": "F-G", "SG-PG": "G", "PF-SF": "F", "SG-SF": "F-G", "PF-C": "C-F", "PG-SG": "G", "C-PF": "C-F", "SG-PG-SF": "F-G", "SF-C": "C-F", "SG-PF": "F-G", "PG-SF": "F-G", "C-SF": "C-F", "SF-PG": "F-G", "G": "G", "F": "F", "C-F": "C-F", "F-C": "C-F", "F-G": "F-G", "G-F": "F-G"}'
    st.code(code2)
    st.caption("Sorry, it was meant to be a multi-line dict...")

    st.markdown("<b>Creating a `seasons_played` column</b>", unsafe_allow_html=True)
    code3_1 = 'player_totals_sort_values = player_totals.sort_values(by=[\'player_id\', \'season\']).head(50)[["season", \'player\', \'experience\']]' 
    code3_2 = 'player_totals_drop_dups = player_totals_sort_values.drop_duplicates(subset=[\'player\', \'season\'])'
    code3_3 = "player_totals_drop_dups_sorted = player_totals_drop_dups.sort_values(by=['player', 'season'])"
    code3_4 = "player_totals_drop_dups_sorted['exp'] = player_totals_drop_dups_sorted.groupby('player').cumcount() + 1"
    code3_5 = "player_totals_simplified = pd.merge(player_totals_sort_values, player_totals_drop_dups_sorted[['player', 'season', 'exp']], on=['player', 'season'], how='left')"
    code3_6 = "player_totals['seasons_played'] = \"Season \" + player_totals['experience'].astype(str)"
    code3 = f'{code3_1}\n{code3_2}\n{code3_3}\n{code3_4}\n{code3_5}\n{code3_6}'
    st.code(code3)

    st.markdown("<b>Drop some columns that are not useful in this project</b>", unsafe_allow_html=True)
    code4_1 = 'CVar = ["season","player_id", "player","ancient_pos","lg","tm", "seasons_played"]'
    code4_2 = 'NVar = ["age","experience","pts","ast","fg","fga","ft","fta","g"]'
    code4_3 = "nba_graph = player_totals[CVar+NVar].copy()"
    code4 = f'{code4_1}\n{code4_2}\n{code4_3}'
    st.code(code4)

    st.markdown('<b>Further drop some more columns</b>', unsafe_allow_html=True)
    code5= 'graph_totals = nba_graph.groupby(CVar)[NVar[2:]].sum().reset_index()'
    st.code(code5)

    st.markdown("<b>Create the column for field goal misses and free throw misses (`fgm` and `ftm` respectively)</b>", unsafe_allow_html=True)
    code6_1 = 'graph_totals["fgm"] = graph_totals["fga"] - graph_totals["fg"]'
    code6_2 = 'graph_totals["ftm"] = graph_totals["fta"] - graph_totals["ft"]'
    code6 = f'{code6_1}\n{code6_2}'
    st.code(code6)

    st.markdown("<b>Create the overall rating of a player in one season, used in later GOAT discussion</b>", unsafe_allow_html=True)
    code7 = 'graph_totals["ovr"] = graph_totals["pts"] + graph_totals["ast"]-graph_totals["fgm"]*0.5 - graph_totals["ftm"]*0.75'
    st.code(code7)

    st.markdown("<b>Create another different dataset containing the mean stats of each player</b>", unsafe_allow_html=True)
    code8 = 'graph_avg = nba_graph.groupby(CVar[1:])[NVar[2:]].mean().reset_index()'
    st.code(code8)

    st.markdown("<b>Team name cleaning</b> (We're almost done!)", unsafe_allow_html=True)
    code9_1 = "team_dict = {\"WSC\": \"WSC\", \"TRH\": \"TRH\", \"STB\": \"STB\", \"PRO\": \"PRO\", 'PIT': 'PIT', \"PHW\": \"GSW\", 'SFW': 'GSW', 'GSW': 'GSW', 'NYK': 'NYK', 'DTF': 'DTF', 'CLR': 'CLR', 'CHS': 'CHS', 'BOS': 'BOS', 'BLB': 'BLB', 'ROC': 'SAC', 'CIN': 'SAC', 'KCO': 'SAC', 'KCK': 'SAC', 'SAC': 'SAC', 'MNL': 'LAL', 'LAL': 'LAL', 'INJ': 'INJ', 'FTW': 'DET', 'DET': 'DET', 'WAT': 'WAT', 'TRI': 'ATL', 'MLH': 'ATL', 'STL': 'ATL', 'ATL': 'ATL', 'SYR': 'PHI', 'PHI': 'PHI', 'SHE': 'SHE', 'INO': 'INO', 'DNN': 'DNN', 'AND': 'AND', 'CHP': 'WAS', 'CHZ': 'WAS', 'BAL': 'WAS', 'CAP': 'WAS', 'WSB': 'WAS', 'WAS': 'WAS', 'CHI': 'CHI', 'SEA': 'OKC', 'OKC': 'OKC', 'SDR': 'HOU', 'HOU': 'HOU', 'PTP': 'PTC', 'MNP': 'PTC', 'PTC': 'PTC', 'OAK': 'VIR', 'WSA': 'VIR', 'VIR': 'VIR', 'NOB': 'MMS', 'MMP': 'MMS', 'MMT': 'MMS', 'MMS': 'MMS', 'NJA': 'BRK', 'NYA': 'BRK', 'NJN': 'BRK', 'BRK': 'BRK', 'MNM': 'FLO', 'MMF': 'FLO', 'FLO': 'FLO', 'KEN': 'KEN', 'IND': 'INA', 'INA': 'INA', 'HSM': 'SSL', 'CAR': 'SSL', 'SSL': 'SSL', 'DNR': 'DEN', 'DEN': 'DEN', 'DLC': 'SAS', 'TEX': 'SAS', 'SAA': 'SAS', 'SAS': 'SAS', 'ANA': 'UTS', 'LAS': 'UTS', 'UTS': 'UTS', 'PHO': 'PHO', 'MIL': 'MIL', 'POR': 'POR', 'CLE': 'CLE', 'BUF': 'LAC', 'SDC': 'LAC', 'LAC': 'LAC', 'SDA': 'SDS', 'NOJ': 'UTA', 'UTA': 'UTA', 'DAL': 'DAL', 'MIA': 'MIA', 'CHH': 'CHO', 'CHA': 'CHO', 'CHO': 'CHO', 'ORL': 'ORL', 'MIN': 'MIN', 'VAN': 'MEM', 'MEM': 'MEM', 'TOR': 'TOR', 'NOH': 'NOP', 'NOK': 'NOP', 'NOP': 'NOP', 'TOT': 'Traded'}"
    code9_2 = "player_totals['present_teams'] = player_totals['tm'].map(team_dict)"
    code9_3 = "graph_avg['present_teams'] = player_totals['tm'].map(team_dict)"
    code9 = f'{code9_1}\n{code9_2}\n{code9_3}'
    st.code(code9)

    st.markdown("<b>Do the same thing for graph_avg dataset</b>", unsafe_allow_html=True)
    code10 = "graph_avg['fgm'] = graph_avg['fga'] - graph_avg['fg']\ngraph_avg['ftm'] = graph_avg['fta'] - graph_avg['ft']\ngraph_avg['ovr'] = graph_avg['pts'] + graph_avg['ast'] - graph_avg['fgm']*0.5 - graph_avg['ftm']*0.75"
    st.code(code10)

    st.markdown("<b>AAAAAND WE ARE DONE!!!</b>", unsafe_allow_html=True)
    st.caption("<i>FINALLY!!!</i>", unsafe_allow_html=True)

# Exploratory Graphs
if s == "Finding the GOAT Player":
    
    tochoose = ["Team-Position", "Position-Team", "Player-Position", "Player-Team"]

    def a (graph_type: str) -> str:
        return f"Click to produce the {graph_type}."
    
    def b (a: str, b: str) -> str:
        return f"ChoiceError: Sorry, for the y-axis column corresponding to the x-axis column \"{a}\", we only support the \"{b}\" column."
    
    def err (msg: str, icon: str = None):
        """
        Displays a streamlit error message, returns a `DeltaGenerator` object (`streamlit.error`)

        Parameters:
        msg (`str`): The error message you want to display using st.error;
        icon (`str`|`None`): The icon for the error message. Default is '🚨';

        Returns:
        `streamlit.error` (`DeltaGenerator`)
        """
        icon = "🚨" if not icon else icon
        return st.error(msg, icon=icon)

    st.title("Exploratory Analysis")
    st.caption("This is where the fun part comes in :)")

#######################################################################################################################################################################

    st.subheader("Visualization of stats across players")
    col7, col8 = st.columns([2,5])
    col7.markdown("Compare stats between the scatter plot and the histograms below ↓")

    with st.form("Scatter"): # TODO: Sync with line 614
        col7_x_input = col7.selectbox("Select a numeric column for the x-axis values", num_dict.values(), key=25)
        col7_y_input = col7.selectbox("Select a numeric column for the y-axis values", np.setdiff1d(list(num_dict.values()), col7_x_input), key=26)
        col7_player = col7.multiselect("Select some players", nba_75, key=27, max_selections=8)
        col7_x = [bname for bname, pname in num_dict.items() if pname == col7_x_input][0]
        col7_y = [bname for bname, pname in num_dict.items() if pname == col7_y_input][0]
        submitted = st.form_submit_button(a("Scatter Plot"))
        # TODO: See if you can find more params to add
        if submitted:
            df = agg(nba_graph)
            df = df[df['player'].isin(col7_player)]
            fig = px.scatter(df, col7_x, col7_y, color='player', labels=all_dict.values(), title="", hover_data=['player', 'season', 'pts'])
            fig.update_traces(marker_line_width=1)
            col8.plotly_chart(fig)

#####################################################################################################################################################################

    st.subheader("Compare stats across players ↓")
    col5, col6 = st.columns([2,5])
    col5.markdown(".") # TODO: Same as line 520

    with st.form("Histogram"): # TODO: Sync with line 583
        col5_x_input = col5.selectbox("Select a numeric column for the x-axis values", np.setdiff1d(list(num_dict.values()), ['Age']), key=17)
        col5_y_input = col5.selectbox("Select a numeric column for the y-axis values", np.setdiff1d(list(num_dict.values()), [col5_x_input]), key=18)
        col5_player = col5.multiselect("Select some players", nba_75, key=19, max_selections=75)
        col5_x = [bname for bname, pname in num_dict.items() if pname == col5_x_input][0]
        col5_y = [bname for bname, pname in num_dict.items() if pname == col5_y_input][0]
        submitted = st.form_submit_button(a("Histogram"))
        histnorm_checkbox = col5.checkbox("Click for a normalized histogram", key=20)
        barmode_checkbox = col5.checkbox("Click for a stack histogram chart", key=21)
        usr_sel_bin_num = col5.checkbox("Do you want to select the number of bins? (Default is 10)", key=22)
        logy = col5.checkbox("Do you want logy?", key=24)
        bins = col5.slider("The amount of bins you want", 5, 35, step=1, key=1002) if usr_sel_bin_num else 10
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        if submitted:
            df = agg(nba_graph)
            df = df[df['player'].isin(col5_player)]
            fig = px.histogram(df, col5_x, col5_y, color='player', histfunc=histfunc, histnorm=histnorm, barmode=barmode, nbins=bins, labels=all_dict, title="", log_y=logy, hover_data=['player', 'ancient_pos'])
            fig.update_traces(marker_line_width=1)
            col6.plotly_chart(fig)

    st.subheader("Compare stats across players for different positions ↓")
    col1, col2 = st.columns([2,5])
    col1.markdown("The histograms show patterns of the players' stats across positions. If you think this is not straightforward, feel free to go back to the scatter plot above and find more.") 

    with st.form("Histogram: 2 numeric; 1 category: position"):  # TODO: Make it better (Sync with line 518)
        # For this one: 2 selectboxes
        col1_x_input = col1.selectbox("Select a numeric column for the x-axis values", np.setdiff1d(list(num_dict.values()), ['Age']), key=1)
        col1_y_input = col1.selectbox("Select a numeric column for the y-axis values", np.setdiff1d(list(num_dict.values()), [col1_x_input, 'Age']), key=2) # type: ignore
        # col1_color_input = col1.selectbox("Select a category column for the color value", cat_dict.values(), key=3)
        # Key value 3 reserved
        col1_x = [bname for bname, pname in num_dict.items() if pname == col1_x_input][0]
        col1_y = [bname for bname, pname in num_dict.items() if pname == col1_y_input][0]
        # col1_color = [bname for bname,pname in cat_dict.items() if pname==col1_color_input][0]
        submitted = st.form_submit_button(a("Histogram"))
        histnorm_checkbox = col1.checkbox("Click for a normalized histogram", key=4)
        barmode_checkbox = col1.checkbox("Click for a stack histogram chart", key=5)
        usr_sel_bin_num = col1.checkbox("Do you want to select the number of bins? (Default is 10)", key=6)
        
        logy = col1.checkbox("Do you want logy?", key=8)
        bins = col1.slider("The amount of bins you want", 5, 35, step=1, key=1000) if usr_sel_bin_num else 10  # Might not work... we'll see
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        if submitted:
            df = agg(nba_graph)
            fig = px.histogram(df, col1_x, col1_y, color='ancient_pos', histnorm=histnorm, barmode=barmode, nbins=bins, labels=all_dict, title="", histfunc=histfunc, log_y=logy)
            fig.update_traces(marker_line_width=1)
            col2.plotly_chart(fig)

    #####
    st.subheader("Box Plot to compare stats for players across different seasons ↓")
    col13, col14 = st.columns([2,5])
    col13.markdown("This is a rather generic plot for showing patterns across stats. Some of the more detailed graphes will be shown (above/below).") # TODO: Describe what kind of info can you get from this

    with st.form("Box"): # TODO: Sync with line 691
        df = nba_graph.copy()
        col13_season = col13.multiselect("Select some seasons", df['season'].unique(), key=49, max_selections=10)
        col13_y_input = col13.selectbox("Select a numeric column for the y-axis values", num_dict.values(), key=50)
        col13_y = [bname for bname, pname in num_dict.items() if pname == col13_y_input][0]
        # Key 51 is reserved
        col13_radio_choice = col13.multiselect("Select some players:", nba_75, key=1551, max_selections=20)
        submitted = st.form_submit_button(a("Box plot"))
        # Key 52 is reserved
        boxmode_checkbox = col13.checkbox("Click for a different boxmode", key=53)
        # Keys 54,55 are ALSO reserved
        logy = col13.checkbox("Do you want logy?", key=56)
        # Key 1006 ALSO reserved
        boxmode = 'relative' if boxmode_checkbox else 'group'
        if submitted:
            choice = 'player'
            # st.write(df.columns)
            df = df[df[choice].isin(col13_radio_choice)]
            df = df[df['season'].isin(col13_season)]
            # st.write(df)
            fig = px.box(df, 'season', col13_y, color=choice, hover_data=['season'], boxmode=boxmode, log_y=logy, height=800, width=600, title="", labels=all_dict.values(), points='all', hover_name=choice)
            fig.update_traces(marker_line_width=1)
            col14.plotly_chart(fig)

    #####
    st.subheader("Box Plot to compare stats for players across different teams ↓")
    col27, col28 = st.columns([2,5])

    with st.form('box2'):
        df = nba_graph.copy()
        col27_team_input = col27.multiselect("Select some teams", df['tm'].unique(), key=129, max_selections=10)
        col27_y_input = col27.selectbox("select a numeric column for the y-axis values", num_dict.values(), key=130)
        col27_player = col27.multiselect("Select some players", nba_75, max_selections=10, key=133)
        col27_team = [bname for bname, pname in team_dict.items() if pname in col27_team_input]
        col27_y = [bname for bname, pname in num_dict.items() if pname == col27_y_input][0]
        submitted = st.form_submit_button(a("Box Plot"))
        boxmode_checkbox = col27.checkbox("Click for a different boxmode", key=131)
        logy = col27.checkbox("Do you want logy?", key=132)
        boxmode = 'relative' if boxmode_checkbox else 'group'
        if submitted:
            df = df[df['tm'].isin(col27_team)]
            df = df[df['player'].isin(col27_player)]
            fig = px.box(df, 'tm', col27_y, color='player', hover_data=['pts', 'ast', 'player', 'season'], boxmode=boxmode, log_y=logy, title="", labels=all_dict.values(), points='all', hover_name='player')
            fig.update_traces(marker_line_width=1)
            col28.plotly_chart(fig)

    st.markdown("<hr>", unsafe_allow_html=True)

    with st.form("Hahaha"):
        hahaha = st.radio("Do you want more box plots?", ['Yes'], key=1000000)
        hahahaha = st.form_submit_button("Produce more!!! CLICK ME CLICK ME!!!")
        if hahahaha:
            st.write("Hmmm... Your keyboard seems to have its own opinions... If this problem persists, please seek for professional help.")



    #########################################################################################################################################################################
    
    st.subheader("Histogram for comparing a player's points/assists across his age ↓")
    col21, col22 = st.columns([2,5])

    with st.form("hisotgram"):
        col21_player = col21.multiselect("Select some players:", nba_75, max_selections=10, key=105)
        pts_or_ast = col21.selectbox("Select a value for the y-axis:", ['Points', 'Assists'], key=106)
        # Keys 107 is reserved
        pts_ast = 'pts' if pts_or_ast == 'Points' else 'ast'
        histnorm_checkbox = col21.checkbox("Click for a normalized histogram", key=108)
        barmode_checkbox = col21.checkbox("Click for a stack histogram chart", key=109)
        usr_sel_bin_num = col21.checkbox("Do you want to select the number of bins? (Default is 10)", key=110)
        logy = col21.checkbox("Do you want logy?", key=111)
        # Key 112 is reserved
        bins = col21.slider("The amount of bins you want", 5, 35, step=1, key=1008) if usr_sel_bin_num else 10  # Might not work... we'll see
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        submitted = st.form_submit_button(a("Hisotgram"))
        if submitted:
            df = nba_graph.copy()
            df = df[df['player'].isin(col21_player)]
            age = df['age']
            fig = px.histogram(df, col21_player, f'{pts_ast}', age, histnorm=histnorm, histfunc=histfunc, barmode=barmode, nbins=bins, log_y=logy, title='`')
            fig.update_traces(marker_line_width=1)
            col22.plotly_chart(fig)

    #########################################################################################################################################################################
        
    ### GENERAL STATS
    st.subheader("Compare avg stats across players ↓")
    st.caption("PS: We'll be using the average dataset for this one!")
    col9, col10 = st.columns([2,5])
    col9.markdown(".") # TODO: Same as line 520

    with st.form("Histogram."): # TODO: Sync with line 631
        col9_x_input = col9.selectbox("Select a numeric column for the x-axis values", num_dict.values(), key=33)
        col9_y_input = col9.selectbox("Select a numeric column for the y-axis values", np.setdiff1d(list(num_dict.values()), col9_x_input), key=34)
        col9_player = col9.multiselect("Select some players", nba_75, key=35, max_selections=20)  # Optional TODO: max selection count may vary from 10 to 20. Will decide later. For now, 20 will do
        col9_x = [bname for bname, pname in num_dict.items() if pname == col9_x_input][0]
        col9_y = [bname for bname, pname in num_dict.items() if pname == col9_y_input][0]
        submitted = st.form_submit_button(a("Histogram"))
        histnorm_checkbox = col9.checkbox("Click for a normalized histogram", key=36)
        barmode_checkbox = col9.checkbox("Click for a stack histogram chart", key=37)
        usr_sel_bin_num = col9.checkbox("Do you want to select the number of bins? (Default is 10)", key=38)
        logy = col9.checkbox("Do you want logy?", key=40)
        bins = col9.slider("The amount of bins you want", 5, 35, step=1, key=1004) if usr_sel_bin_num else 10  # Might not work... we'll see
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        if submitted:
            df = agg(nba_graph, ['player', 'ancient_pos', 'present_teams'], 'mean')
            df = df[df['player'].isin(col9_player)]
            fig = px.histogram(df, col9_x, col9_y, color='player', histfunc=histfunc, histnorm=histnorm, barmode=barmode, nbins=bins, labels=all_dict.values(), title="", log_y=logy)
            fig.update_traces(marker_line_width=1)
            col10.plotly_chart(fig)

    ########################################################################################################################################################################

    st.subheader("Line plot for comparing stats across players ↓")
    col15, col16 = st.columns([2,5])

    with st.form("Line"): # TODO: Sync with Line 749
        # TODO: Not DYNAMIC INPUT, use player exp. (Season 1, 2, ...) not years
        col15_pos_input = col15.selectbox("Pick a position", ['Center', 'Forward', 'Guard'], key=57)
        if col15_pos_input == 'Center':
            valid = nba_graph[nba_graph['ancient_pos'].isin(['C', 'C-F'])]
        elif col15_pos_input == 'Forward':
            valid = nba_graph[nba_graph['ancient_pos'].isin(['F', 'F-G'])]
        else:
            valid = nba_graph[nba_graph['ancient_pos'].isin(['G', 'G-F'])]
        col15_y_input = col15.selectbox("Select a numeric column for the y-axis values", np.setdiff1d(list(num_dict.values()), ['Years of Experience', 'Season']), key=58)
        col15_player = col15.multiselect("Select some players", valid['player'].unique(), max_selections=10, key=59)
        # col15_x = [bname for bname, pname in num_dict.items() if pname == col15_x_input][0]
        col15_y = [bname for bname, pname in num_dict.items() if pname == col15_y_input][0]
        # Keys 60~63 are reserved
        logy = col15.checkbox("Do you want logy?", key=64)
        submitted = st.form_submit_button(a("Line Plot"))
        if submitted:
            df = agg(nba_graph, ['player', 'experience'])
            df = df[df['player'].isin(col15_player)].sort_values('experience')
            fig = px.line(df, 'experience', col15_y, color='player', title=".", labels=all_dict.values(), log_y=logy)
            fig.update_traces(marker_line_width=1)
            col16.plotly_chart(fig)

    #########################################################################################################################################################################

    st.subheader("Sunburst Plot for comparing stats across teams and players ↓")
    col17, col18 = st.columns([2,5])
    ### PLAYER-TEAM
    with st.form("Sunburst"):
        # choice = col17.selectbox("Select the columns you want to show in this graph: (Format: inner_circle-outer_circle)", tochoose, key=1601)
        numcol_input = col17.selectbox("Select a numeric column:", num_dict.values(), key=86)
        numcol = [bname for bname, pname in num_dict.items() if pname == numcol_input][0]
        df1 = agg(nba_graph, ['tm', 'ancient_pos', 'player'])
        df1 = df1[(df1['player'].isin(nba_75)) & (df1['tm'].isin(team_dict.keys()))]
        df1['tm'] = df1['tm'].replace(team_dict)
        df1['ancient_pos'] = df1['ancient_pos'].replace(pos_dict)
        # if choice == "Team-Position":  # Team-Pos
        col17_team_input = col17.multiselect("Select some teams:", df1['tm'].unique(), key=65, max_selections=10)
        df1 = df1[df1['tm'].isin(col17_team_input)]
        col17_pos_input = col17.multiselect("Select some positions:", df1['ancient_pos'].unique(), key=66)
        bool_idx = (df1['tm'].isin(col17_team_input)) & (df1['ancient_pos'].isin(col17_pos_input))
        sppath = ['tm', 'ancient_pos', 'player']
        submitted = st.form_submit_button(a("Sunburst Plot"))
        if submitted:
            fig1 = px.sunburst(df1[bool_idx], values = numcol, path=sppath, height=800, width=600)
            col18.plotly_chart(fig1)
           
    #########################################################################################################################################################################
    # TODO: Change ALL to LINE PLOTS!
    st.subheader("Histogram for comparing a player's overall score across his age ↓")
    col19, col20 = st.columns([2,5])

    with st.form("Histogram1......"):
        col19_player = col19.multiselect("Select some players:", nba_75, max_selections=10, key=97)
        # Keys 98 and 99 are reserved
        histnorm_checkbox = col19.checkbox("Click for a normalized histogram", key=100)
        barmode_checkbox = col19.checkbox("Click for a stack histogram chart", key=101)
        usr_sel_bin_num = col19.checkbox("Do you want to select the number of bins? (Default is 10)", key=102)
        logy = col19.checkbox("Do you want logy?", key=103)
        mean_or_sum = col19.checkbox("Click if you want `sum` (default is `mean`)", key=104)
        bins = col19.slider("The amount of bins you want", 5, 35, step=1, key=1007) if usr_sel_bin_num else 10  # Might not work... we'll see
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        submitted = st.form_submit_button(a("Histogram"))
        mean_sum = 'sum' if mean_or_sum else 'mean'
        if submitted:
            df = agg(nba_graph, ['age', 'player'], mean_sum)
            fig = px.histogram(df[df['player'].isin(col19_player)], 'age', 'ovr', 'player', histnorm=histnorm, histfunc=histfunc, barmode=barmode, nbins=bins, log_y=logy, title='')
            fig.update_traces(marker_line_width=1)
            col20.plotly_chart(fig)

    #########################################################################################################################################################################
    #####
    ### PLAYER-EXP (GOAT PLAYER)
    st.subheader("Histogram for comparing a player's 2-pointers/3-pointers made across his age ↓")
    col23, col24 = st.columns([2,5])
    # Player vs x2p, x3p, color = age
    with st.form("Histogram:"):
        col23_player = col23.multiselect("Select some players", nba_75, max_selections = 10, key=113)
        histnorm_checkbox = col23.checkbox("Click for a normalized histogram", key=114)
        barmode_checkbox = col23.checkbox("Click for a stack histogram chart", key=115)
        usr_sel_bin_num = col23.checkbox("Do you want to select the number of bins? (Default is 10)", key=116)
        logy = col23.checkbox("Do you want logy?", key=117)
        x2p_x3p = col23.selectbox("Select a value for the y-axis:", ['x2p', 'x3p'], key=118)
        # x2p_x3p = 'x2p' if x2p_or_x3p == 'x2p' else 'x3p'
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        submitted = st.form_submit_button(a("Hisotgram"))
        if submitted:
            df1 = agg(nba_graph, ['player', f'{x2p_x3p}'])
            df1 = df1[df1['player'].isin(col23_player)]
            fig = px.histogram(df1, 'player', f'{x2p_x3p}', 'age', histnorm=histnorm, histfunc=histfunc, barmode=barmode, nbins=bins)
            fig.update_traces(marker_line_width=1)
            col24.plotly_chart(fig)
    
    #########################################################################################################################################################################
###########################################


if s == 'Analysis for some of the Greatest Teams of All Time':
    def a (graph_type: str) -> str:
        return f"Click to produce the {graph_type}."
    
    st.subheader("Exploratory for comparing two teams in a season ↓")
    ### GOAT TEAM
    col29, col30 = st.columns([4, 8])
    # st.text("You might ONLY see the multiselect box of the two teams. This is because the code uses an if statement to check the length of the selected list.", help='You may also see a \'Missing form submit button\' (or is it only ME from the pre-deploy page?), this is alright. You can see the button after 2 teams is selected.')

    with st.form("XXX"):
        col29_team_input_1 = col29.selectbox("Select first team", team_dict.values(), key=137)
        col29_team_input_2 = col29.selectbox("Select second team", np.setdiff1d(list(team_dict.values()), col29_team_input_1), key=138)
        # if len(col29_team_input) == 2:
        team_1, team_2 = col29_team_input_1, col29_team_input_2
        filtered_data = nba_graph[nba_graph['ptn'].isin([team_1, team_2])]
        valid_seasons = filtered_data.groupby('ptn')['season'].apply(set).to_dict()
        if team_1 in valid_seasons and team_2 in valid_seasons:
            common_seasons = valid_seasons[team_1].intersection(valid_seasons[team_2])
            if len(common_seasons) > 0:
                col29_season_input = col29.selectbox("Select a season", sorted(common_seasons), key=134)
                final_df = filtered_data[filtered_data['season'] == col29_season_input]
                yaxis_data = col29.selectbox("Select y-axis stat", NVar[1:], key=135)
                textposition_outside = col29.selectbox("Text outside bars? (Recommended: YES)", ["Yes", "No"], key=136)
                textpos = "outside" if textposition_outside == "Yes" else "inside"
                submitted = st.form_submit_button(a("Bar chart"))
                if submitted:
                    fig = px.bar(final_df, x="player", y=yaxis_data, color="ptn", text_auto=True, height=600, width=800)
                    fig.update_traces(textposition=textpos, texttemplate="<b>%{y:.2f}</b>")
                    fig.update_xaxes(categoryorder="total descending", matches=None, showticklabels=True, tickangle=45)
                    col30.plotly_chart(fig)
            else:
                st.error(f"The selected teams ({team_1} and {team_2}) do not share any common seasons.")  # noqa: E701
        else:
            st.error(f"One or both teams ({team_1} and {team_2}) do not exist in the dataset.") # noqa: E701
        # else:
        #   st.info("Please select exactly 2 teams to proceed.") # noqa: E701

    st.subheader("Sunburst Plot for comparing stats for teams and seasons ↓")
    col25, col26 = st.columns([2,5])

    with st.form("?"):
        numcol_input = col25.selectbox("Select a numeric column:", np.setdiff1d(list(num_dict.values()), 'Season'), key=119)
        numcol = [bname for bname, pname in num_dict.items() if pname == numcol_input][0]
        df1 = agg(nba_graph, ['tm', 'ancient_pos', 'season'])
        df1 = df1[df1['tm'].isin(team_dict.keys())]
        df1['tm'] = df1['tm'].replace(team_dict)
        col25_team_input = col25.multiselect("Select some teams:", df1['tm'].unique(), key=120, max_selections=10)
        df1 = df1[df1['tm'].isin(col25_team_input)]
        col25_season_input = col25.multiselect("Select some seasons:", df1['season'].unique(), key=121)
        bool_idx = (df1['tm'].isin(col25_team_input)) & (df1['season'].isin(col25_season_input))
        sppath = ['tm', 'season'] 
        submitted = st.form_submit_button(a("Sunburst"))
        if submitted:
            fig1 = px.sunburst(df1[bool_idx], values=numcol, path=sppath, height=800, width=600)
            col26.plotly_chart(fig1)


    st.subheader("Compare avg stats across teams ↓")
    st.caption("`graph_avg` will also be used for this one!")
    col11, col12 = st.columns([2,5])

    with st.form("Histogram.."): # TODO: Sync with line 659
        col11_x_input = col11.selectbox("Select a numeric column for the x-axis values", num_dict.values(), key=41)
        col11_y_input = col11.selectbox("Select a numeric column for the y-axis values", np.setdiff1d(list(num_dict.values()), col11_x_input), key=42)
        col11_team_input = col11.multiselect("Select some teams", team_dict.values(), key=43, max_selections=20) # Optional TODO: same as line 599
        col11_x = [bname for bname, pname in num_dict.items() if pname == col11_x_input][0]
        col11_y = [bname for bname, pname in num_dict.items() if pname == col11_y_input][0]
        col11_team = [bname for bname, pname in team_dict.items() if pname in col11_team_input]
        histnorm_checkbox = col11.checkbox("Click for a normalized histogram", key=44)
        barmode_checkbox = col11.checkbox("Click for a stack histogram chart", key=45)
        usr_sel_bin_num = col11.checkbox("Do you want to select the number of bins? (Default is 10)", key=46)
        logy = col11.checkbox("Do you want logy?", key=48)
        bins = col11.slider("The amount of bins you want", 5, 35, step=1, key=1005) if usr_sel_bin_num else 10  # Might not work... we'll see
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        submitted = st.form_submit_button(a("Histogram"))
        if submitted:
            x11 = agg(nba_graph, ['player', 'ancient_pos', 'present_teams'], 'mean')
            x11 = x11[x11['present_teams'].isin(col11_team)]
            fig = px.histogram(x11, col11_x, col11_y, color='present_teams', histfunc=histfunc, histnorm=histnorm, barmode=barmode, nbins=bins, labels=all_dict.values(), title="", log_y=logy)
            fig.update_traces(marker_line_width=1)
            col12.plotly_chart(fig)


    st.subheader("Histogram of comparing stats across different teams ↓")
    col3, col4 = st.columns([2,5])
    col3.markdown("") # TODO: Same as line 520

    with st.form("Histogram: 2 numeric; Category: Team"): # TODO: Sync with line 549
        col3_x_input = col3.selectbox("Select a numeric column for the x-axis values", np.setdiff1d(list(num_dict.values()), ['Age']), key=9)
        col3_y_input = col3.selectbox("Select a numeric column for the y-axis values", np.setdiff1d(list(num_dict.values()), [col3_x_input, 'Age']), key=10) # type: ignore
        col3_team_input = col3.multiselect("Select some team names", team_dict.values(), key=11, max_selections=10)
        col3_x = [bname for bname, pname in num_dict.items() if pname == col3_x_input][0]
        col3_y = [bname for bname, pname in num_dict.items() if pname == col3_y_input][0]
        col3_team = [bname for bname,pname in team_dict.items() if pname in col3_team_input]
        submitted = st.form_submit_button(a("Histogram"))
        histnorm_checkbox = col3.checkbox("Click for a normalized histogram", key=12)
        barmode_checkbox = col3.checkbox("Click for a stack histogram chart", key=13)
        usr_sel_bin_num = col3.checkbox("Do you want to select the number of bins? (Default is 10)", key=14)
        logy = col3.checkbox("Do you want logy?", key=16)
        bins = col3.slider("The amount of bins you want", 5, 35, step=1, key=1001) if usr_sel_bin_num else 10  # Might not work... we'll see
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        if submitted:
            # st.write(col3_team)
            df = agg(nba_graph, ['present_teams'])
            # st.write(df)
            df = df[df['present_teams'].isin(col3_team)]
            # st.write(df)
            fig = px.histogram(df, col3_x, col3_y, color='present_teams', histfunc=histfunc, histnorm=histnorm, barmode=barmode, nbins=bins, labels=all_dict, title="", log_y=logy)
            fig.update_traces(marker_line_width=1)
            col4.plotly_chart(fig)
    
    # Optional TODO: Facet Plots

# Analysis
if s == "Analysis of GOAT by stats for the ten most popular players":
    st.title("Analysis of GOAT by stats for the ten most popular players")
    st.subheader("We'll be foucsing on the analysis for the ten most popular GOAT nominees: Lebron James, Michael Jordan, Kobe Bryant, Steph Curry and Magic Johnson, and")
    st.subheader("Larry Bird, Kareem Abdul-Jabbar, Tracy McGrady, Bill Russell and Wilt Chamberlain.")
    st.text("Note that because Bill Russell and Wilt Chamberlain are from the old days (1960s), some of their data are not included in the original dataset.")
    
    # DataFrame Creation
    ana_df = player_totals.copy()
    ana_df = ana_df[ana_df['player'].isin(['LeBron James', 'Michael Jordan', 'Kobe Bryant', 'Stephen Curry', 'Magic Johnson', 'Larry Bird', 'Kareem Abdul-Jabbar', 'Tracy McGrady', 'Bill Russell', 'Wilt Chamberlain'])]

    ana_corr_df = ana_df.copy()
    ana_corr_results = {p: ana_corr_df.loc[ana_corr_df['player'] == p , ['per', 'ovr']].corr().loc['per', 'ovr'] for p in ana_corr_df['player'].unique()}
    ana_corr_df = pd.Series(ana_corr_results).reset_index().rename({'index':'Player Name', 0:'Correlation'}, axis=1).sort_values('Correlation', ascending=False).reset_index(drop=True)
    # TODO: Select ten of the best seasons of each player, and add a markdown explaining Why 10.

    ana_df['off_totals'] = ana_df['pts'] + ana_df['ast'] + ana_df['orb']
    ana_df['off_per_game'] = ana_df['ppg'] + ana_df['apg'] + ana_df['orpg']

    ana_df['def_totals'] = ana_df['stl'] + ana_df['blk'] + ana_df['drb']
    ana_df['def_per_game'] = ana_df['spg'] + ana_df['bpg']+ ana_df['drpg']

    ana_df['comb_totals'] = ana_df['off_totals'] + ana_df['def_totals']
    ana_df['comb_per_game'] = ana_df['off_per_game'] + ana_df['def_per_game']

    ana_var_dict = {
        'off_totals':'Offensive Totals',
        'off_per_game':"Offense Per Game",
        'def_totals':'Defensive Totals',
        'def_per_game':'Defense Per Game',
        'comb_totals':'Combined Totals',
        'comb_per_game':'Combined Per Game'
    }
    pretty_dict = ana_var_dict.update(num_dict)

    off_list = ['off_totals', 'off_per_game']
    def_list = ['def_totals', 'def_per_game']
    comb_list = ['comb_totals', 'comb_per_game']
    off_raw = ['pts', 'ast', 'orb']
    def_raw = ['stl', 'blk', 'drb']
    off_avg = ['ppg', 'apg', 'orpg']
    def_avg = ['spg', 'bpg', 'drpg']
    all_list = off_list + def_list + comb_list + off_raw + def_raw + off_avg + def_avg

    ana_long = ana_df.melt(['player'], 
                           all_list, 
                           'stat_type', 
                           'value'
    )
    ana_long['meas'] = ana_long['stat_type'].replace(ana_var_dict)

############

    st.subheader("Analyzing Offensive stats ↓")
    st.markdown("We'll be looking at a facet plot with stats (per game also) first:")
    ac1, ac2 = st.columns([4,6])
    ac1.markdown("Here's the analysis for the ten players' offensive stats:")
    ac1.markdown("We can clearly see that LeBron leads both the Totals and the Per Game chart <b>BY A LOT</b>", unsafe_allow_html=True)
    ac1.markdown("Tracy McGrady is the last all two charts.")
    ac1.markdown("Interestingly, both of Jordan's score was less than Kobe. But he still ranked the 3rd.")
    af1 = px.histogram(
        ana_long[ana_long['stat_type'].isin(off_list)], 
        'player', 
        'value', 
        'meas', 
        None, 
        None, 
        'meas', 
        facet_col_spacing=0.1,
        title="NBA Player Stats: Offensive", 
        height=800, 
        text_auto=True
    )
    af1.update_layout(
        yaxis_title="Value", 
        showlegend=True, 
        legend_title_text="Stat Type"
    )
    af1.update_xaxes(title='Player Name')
    af1.update_yaxes(matches=None, showticklabels=True)
    af1.update_traces(textposition='outside', texttemplate='<b>%{y:.3s}</b>')
    af1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    ac2.plotly_chart(af1)

    st.subheader("Analyzing Defensive stats ↓")
    ac3, ac4 = st.columns([4,5])
    ac3.markdown("Here's the analysis for the ten players' defensive stats:")
    af2 = px.histogram(
        ana_long[ana_long['stat_type'].isin(def_list)],
        'player',
        'value',
        'meas',
        None,
        None,
        'meas',
        facet_col_spacing=0.1,
        title="NBA Player Stats: Defensive",
        height=800,
        text_auto=True
    )
    af2.update_layout(
        yaxis_title="Value",
        showlegend=True,
        legend_title_text="Stat Type"
    )
    af2.update_xaxes(title='Player Name')
    af2.update_yaxes(matches=None, showticklabels=True)
    af2.update_traces(textposition='outside', texttemplate='<b>%{y:.3s}</b>')
    af2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    ac4.plotly_chart(af2)
    ac3.markdown("Unsurprisingly, Kareem leads the defensive stats on the Totals.")
    ac3.markdown("What IS surprising: LeBron narrowing Kareen by 5 in the Per Game!")
    ac3.markdown("Not surprisingly, Steph Curry is the lowest of all. (I mean, it is quite reasonable")
    st.subheader("Analyzing all (combined) stats ↓")
    # Combined = Offensive + Defensive
    ac5, ac6 = st.columns([4,5])
    ac5.markdown("Here's the analysis for the ten players' combined stats:")
    af3 = px.histogram(
        ana_long[ana_long['stat_type'].isin(comb_list)],
        'player',
        'value',
        'meas',
        None,
        None,
        'meas',
        0,
        None,
        0.1,
        title="NBA Player Stats: Combined",
        height=800,
        text_auto=True
    )
    af3.update_layout(
        yaxis_title="Value",
        showlegend=True,
        legend_title_text="Stat Type"
    )
    af3.update_xaxes(title='Player Name')
    af3.update_yaxes(matches=None, showticklabels=True)
    af3.update_traces(textposition='outside', texttemplate='<b>%{y:.3s}</b>')
    af3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    ac6.plotly_chart(af3)
    ac5.markdown("So, to sum it up:")
    ac5.markdown("LeBron, undoubtly, lands on 1st.")
    ac5.markdown("Kobe beats Jordan and secured himself a 2nd place.")
    ac5.markdown("And here's the best part: Kareem beat Michael by 1.3k in the totals but lost to him by 19 in the Per Game (which turns out to be the 3rd, 4th decider)")

    st.markdown("<hr style=\"height: 5px; background-color: red;\" />", unsafe_allow_html=True)

    # TODO: More raw graphs
    ac7, ac8 = st.columns([6,6])
    af4 = px.histogram(
        ana_long[ana_long['stat_type'].isin(off_raw)],
        'player',
        'value',
        'meas',
        None,
        'meas',
        facet_row_spacing=0.1,
        title='NBA Player Stats: Offensive Raw',
        height=600,
        text_auto=True
    )
    af4.update_layout(
        yaxis_title="Value",
        showlegend=True,
        legend_title_text="Stat Type"
    )
    af4.update_xaxes(title='Player Name')
    af4.update_yaxes(matches=None, showticklabels=True)
    af4.update_traces(textposition='inside', texttemplate='<b>%{y:.3s}</b>')
    af4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    ac7.plotly_chart(af4)

    af5 = px.histogram(
        ana_long[ana_long['stat_type'].isin(def_raw)],
        'player',
        'value',
        'meas',
        None,
        'meas',
        facet_row_spacing=0.1,
        title='NBA Player Stats: Defensive Raw',
        height=600,
        text_auto=True
    )
    af5.update_layout(
        yaxis_title="Value",
        showlegend=True,
        legend_title_text="Stat Type"
    )
    af5.update_xaxes(title='Player Name')
    af5.update_yaxes(matches=None, showticklabels=True)
    af5.update_traces(texttemplate='<b>%{y:.3s}</b>')
    af5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    ac8.plotly_chart(af5)

    st.write("As we can see, LeBron James leads the raw stats for points and assists, and Kareem, as it can be seen through the graph, leads in the Offensive Rebounds (ORB).")
    st.write("MJ leads the steals and Kareem leads the blocks and the Defensive Rebounds (DRB). (Reasonable, since he's the only Center in this graph)")
    st.write("Overall (in this map), LeBron leads the offensive stats and Kareem leads the defensive stats (including offensive rebounds), with MJ a single lead in the steals.")
    st.write("T-Mac is still the worst in offensive stats but he is better than Steph Curry in the rebounds and defensive stats.")

    ac9, ac10 = st.columns([6,6])
    af6 = px.histogram(
        ana_long[ana_long['stat_type'].isin(off_avg)],
        'player',
        'value',
        'meas',
        None,
        'meas',
        facet_row_spacing=0.1,
        title='NBA Player Stats: Offensive Average',
        height=600,
        text_auto=True
    )
    af6.update_layout(
        yaxis_title="Value",
        showlegend=True,
        legend_title_text="Stat Type"
    )
    af6.update_xaxes(title='Player Name')
    af6.update_yaxes(matches=None, showticklabels=True)
    af6.update_traces(textposition='inside', texttemplate='<b>%{y:.3s}</b>')
    af6.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    ac9.plotly_chart(af6)

    af7 = px.histogram(
        ana_long[ana_long['stat_type'].isin(def_avg)],
        'player',
        'value',
        'meas',
        None,
        'meas',
        facet_row_spacing=0.1,
        title='NBA Player Stats: Defensive Average',
        height=600,
        text_auto=True
    )
    af7.update_layout(
        yaxis_title="Value",
        showlegend=True,
        legend_title_text="Stat Type"
    )
    af7.update_xaxes(title='Player Name')
    af7.update_yaxes(matches=None, showticklabels=True)
    af7.update_traces(texttemplate='<b>%{y:.3s}</b>')
    af7.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    ac10.plotly_chart(af7)

    st.markdown("<hr style=\"height: 5px; background-color: red;\" />", unsafe_allow_html=True)
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    st.text("From that, I think it's safe to say that LeBron James is the NBA GOAT in this analysis section.", help="Although, any disagreement is okay. But feel free to go back and look at the graphs yourselves!")
    st.markdown("Here's a detailed analysis:")
    st.markdown("To begin, LBJ leads the Offensive stats (both the Totals and the Per Game chart)")
    st.markdown("Second, LBJ is an excellent Defensive player. Those who have seen his most iconic plays must have been impressed by his defensive talents. Looking at the data, we can find him second in the Defensive Totals, and top in the Per Game.")
    st.markdown("Focusing back on reality, he has 4 championship rings (including one when he beat the 73-9 \"Super Warriors\" in 2016). He is one of the few to have more than 3 rings.")
    st.markdown("Furthermore, his 20-year long-lasting career makes him an icon in the three decades he played in.")
    st.text("It is also worth noting that because of the lack of data, we cannot provide a further analysis of the Play-making data of these players. (But it is foreseeable that Magic and Bird will excel in these stats)")

if s == "Analysis of the NBA Championship teams in iconic seasons":
    st.title("Analysis of the NBA Championship teams in iconic seasons (eg: 1995 Bulls, 1986 Celtics, etc.)")

    # (Re) Create the dataset with minor adjustments
    ana_df = player_totals.copy()
    ana_df['off_totals'] = ana_df['pts'] + ana_df['ast'] + ana_df['orb']
    ana_df['off_per_game'] = ana_df['ppg'] + ana_df['apg'] + ana_df['orpg']
    ana_df['def_totals'] = ana_df['stl'] + ana_df['blk'] + ana_df['drb']
    ana_df['def_per_game'] = ana_df['spg'] + ana_df['bpg']+ ana_df['drpg']
    ana_df['comb_totals'] = ana_df['off_totals'] + ana_df['def_totals']
    ana_df['comb_per_game'] = ana_df['off_per_game'] + ana_df['def_per_game']
    ana_var_dict = {
        'off_totals':'Offensive Totals',
        'off_per_game':"Offense Per Game",
        'def_totals':'Defensive Totals',
        'def_per_game':'Defense Per Game',
        'comb_totals':'Combined Totals',
        'comb_per_game':'Combined Per Game'
    }
    pretty_dict = ana_var_dict.update(num_dict)

    st.subheader("1. 1996 Bulls")
    bulls_96 = ana_df.copy()
    bulls_96 = bulls_96[bulls_96['season'] == 1996]
    bulls_96 = bulls_96[bulls_96['tm'] == 'CHI'].reset_index(drop=True)
    # st.write(bulls_95)
    # st.write(bulls_95[bulls_95['player'] == 'Michael Jordan'])
    bulls, bulls2 = st.columns([6,10])
    ag = px.bar(bulls_96, 'player', 'per', 'ancient_pos', hover_data=['pts', 'ast', 'ovr'], height=800, width=1000)
    ag.update_layout(yaxis=dict(showticklabels=False))
    ag.update_yaxes(title='Player Efficiency Ratings of This Season')
    ag.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>', outsidetextfont_family='Times New Roman')
    ag.update_layout(bargap=0.3)
    ag.update_xaxes(categoryorder='total descending')
    for trace in ag.data:
        text_values = []
        for i, value in enumerate(trace.y):
            text_value = f'{value:.2f}'
            text_values.append(text_value)
        if trace.text is not None:
            trace.text = text_values
    bulls2.plotly_chart(ag)
    bulls.markdown("Rodman, Pippen and MJ all ended up with a PER over 20, and MJ's PER is over 30!")

    # st.markdown("<hr style=\"height: 5px; background-color: red;\" />", unsafe_allow_html=True)

    st.subheader("1986 Celtics")
    celts_86 = ana_df.copy()
    celts_86 = celts_86[celts_86['season'] == 1986]
    celts_86 = celts_86[celts_86['tm'] == 'BOS']
    celts, celts2 = st.columns([6,10])
    ag2 = px.bar(celts_86, 'player', 'per', 'ancient_pos', hover_data=['pts', 'ast', 'ovr'], text_auto=True)
    ag2.update_yaxes(title='Player Efficiency Ratings of This Season')
    ag2.update_xaxes(categoryorder='total descending')
    ag2.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    celts2.plotly_chart(ag2)
    celts.markdown("Unsurprisingly, the only three players with a PER greater than 20 are the 'Big Three' of the time: Larry Bird, Robert Parish and Kevin McHale.")
    celts.markdown("Undoubtedly, Larry Bird is the absolute STAR on this team.")

    st.subheader("3. 1987 Lakers")
    lakers_87 = ana_df.copy()
    lakers_87 = lakers_87[(lakers_87['season'] == 1987) & (lakers_87['tm'] == 'LAL')]
    lakers, lakers2 = st.columns([6,10])
    ag3 = px.bar(lakers_87, 'player', 'per', 'ancient_pos', hover_data=['pts', 'ast', 'ovr'], text_auto=True)
    ag3.update_yaxes(title='Player Efficiency Ratings of This Season')
    ag3.update_xaxes(categoryorder='total descending')
    ag3.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    lakers2.plotly_chart(ag3)
    lakers.markdown("Magic Johnson had a 35.5 PER this season, and this trio (Magic, James Worthy, and Kareem) were also the only three players to have a PER greater than 20 in the team.")

    st.subheader("4. 2008 Celtics")
    celts_08 = ana_df.copy()
    celts_08 = celts_08[(celts_08['season'] == 2008) & (celts_08['tm'] == 'BOS')]
    celts3, celts4 = st.columns([6,10])
    ag4 = px.bar(celts_08, 'player', 'per', 'ancient_pos', hover_data=['pts', 'ast', 'ovr'], text_auto=True)
    ag4.update_yaxes(title='Player Efficiency Ratings of This Season')
    ag4.update_xaxes(categoryorder='total descending')
    ag4.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    celts4.plotly_chart(ag4)
    celts3.markdown("Paul Pierce and Kevin Garnett both have a PER of over 22.")
    celts3.markdown("And although it is said that Paul, Kevin and Ray make the trio up, it turns out that Ray's PER (17.5) is only 1 above that of Rajon Rondo's (16.1)")

    st.subheader("5. 1983 76ers")
    sixers_83 = ana_df.copy()
    sixers_83 = sixers_83[(sixers_83['season'] == 1983) & (sixers_83['tm'] == 'PHI')]
    sixers, sixers2 = st.columns([6,10])
    ag5 = px.bar(sixers_83, 'player', 'per', 'ancient_pos', hover_data=['pts', 'ast', 'ovr'], text_auto=True)
    ag5.update_yaxes(title='Player Efficiency Rating of This Season')
    ag5.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    ag5.update_xaxes(categoryorder='total descending')
    sixers2.plotly_chart(ag5)
    sixers.markdown('Dr. J (Julius Erving) and Moses Malone both have their PER above 25, with the latter ending up with a stunning 33.5!')

    st.subheader('6. 2001 Lakers')
    lakers_01 = ana_df.copy()
    lakers_01 = lakers_01[(lakers_01['season'] == 2001) & (lakers_01['tm'] == 'LAL')]
    lakers3, lakers4 = st.columns([6,10])
    ag6 = px.bar(lakers_01, 'player', 'per', 'ancient_pos', hover_data=['pts', 'ast', 'ovr'], text_auto=True)
    ag6.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    ag6.update_yaxes(title='Player Efficiency Ratings of This Season')
    ag6.update_xaxes(categoryorder='total descending')
    lakers4.plotly_chart(ag6)
    lakers3.markdown("Shaq ended up with a 33.9 PER and Kobe with a 28.5.")
    lakers3.markdown("No other player had their PER above 15. (The closest to that was Derrick Fisher and Horace Grant, with 14.7 and 14.16 respectively)")

    st.subheader('7. 2016 Cavaliers')
    cavs_16 = ana_df.copy()
    cavs_16 = cavs_16[(cavs_16['season'] == 2016) & (cavs_16['tm'] == 'CLE')]
    cavs, cavs2 = st.columns([6,10])
    ag8 = px.bar(cavs_16, 'player', 'per', 'ancient_pos', hover_data=['pts', 'ast', 'ovr'], text_auto=True)
    ag8.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    ag8.update_yaxes(title='Player Efficiency Ratings of This Season')
    ag8.update_xaxes(categoryorder='total descending')
    cavs2.plotly_chart(ag8)
    cavs.markdown("Only LeBron and Kevin Love's PER are above 20 (While Erving's was 19.1)")

    st.markdown("<hr style=\"height: 5px; background-color: red;\" />", unsafe_allow_html=True)

    champ_df = pd.concat([sixers_83, celts_86, lakers_87, bulls_96, lakers_01, celts_08, cavs_16], ignore_index=True)
    champ_df['team_seas'] = champ_df['tm'] + ' ' + champ_df['season'].astype(str).str[2:]
    champ_avg = champ_df.groupby(['team_seas'])[['per', 'pts', 'ast', 'ovr', 'trb']].mean().reset_index()
    # st.write(champ_avg)
    ag7 = px.bar(champ_avg, 'team_seas', 'per', 'team_seas', hover_data=['pts', 'ast', 'trb'], text_auto=True)
    ag7.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    ag7.update_yaxes(title='Average Player Efficiency Ratings')
    ag7.update_xaxes(categoryorder='total descending')
    champ, champ2 = st.columns([6,10])
    champ2.plotly_chart(ag7)

    champ_df.loc[(champ_df['player'] == 'Ron Harper') & (champ_df['tm'] == 'CHI'), 'player'] = 'Ron Harper (Bulls)'
    champ_df.loc[(champ_df['player'] == 'Ron Harper') & (champ_df['tm'] == 'LAL'), 'player'] = 'Ron Harper (Lakers)'

    champ_compare = px.bar(champ_df, x='player', y='per', color='team_seas', facet_col='pos', height=1500, width=2000, facet_col_wrap=2, facet_col_spacing=0.02, facet_row_spacing=0.08, text_auto=True)
    champ_compare.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    champ_compare.update_yaxes(showticklabels=True)
    champ_compare.update_xaxes(categoryorder='total descending', matches=None, showticklabels=True, tickangle=45)
    st.plotly_chart(champ_compare)

    # st.html("<hr style=\"height: 5px; background-color: red;\" />")
    st.markdown("A SMALL CONCLUSION ↓")
    st.text("In the individual PER ratings, Magic Johnson stands out with his 35.54.")
    st.text("And as for the average PER, here is a table of the teams and their averaging PER:")
    st.text("""
    season + team name  | average PER (4 d.p.)
    --------------------|---------------------------------
    1996 Bulls          | 10.6553
    1986 Celtics        | 12.8308
    1987 Lakers         | 13.8000
    2008 Celtics        | 10.7387
    1983 76ers          | 12.5286
    2001 Lakers         | 11.0073
    2016 Cavaliers      | 10.2206
    """)
    st.text("The 1987 Lakers somehow leads the average PER (Probably because of Magic).")
    
if s == 'Rivalry Team Comparison':
    st.title("Rivalry Team Comparison")
    st.header('We are analyzing some of the rivalry teams in some NBA Finals (eg: 2016 Warriors vs Cavs; 2001 76ers vs Lakers; etc.)')
    st.markdown("We are comparing the PER of the players in these rival teams.")
    st.text('\n')
    # (For the third time) Create the dataset (with minor adjustments)
    ana_df = player_totals.copy()
    ana_df['off_totals'] = ana_df['pts'] + ana_df['ast'] + ana_df['orb']
    ana_df['off_per_game'] = ana_df['ppg'] + ana_df['apg'] + ana_df['orpg']
    ana_df['def_totals'] = ana_df['stl'] + ana_df['blk'] + ana_df['drb']
    ana_df['def_per_game'] = ana_df['spg'] + ana_df['bpg']+ ana_df['drpg']
    ana_df['comb_totals'] = ana_df['off_totals'] + ana_df['def_totals']
    ana_df['comb_per_game'] = ana_df['off_per_game'] + ana_df['def_per_game']
    ana_var_dict = {
        'off_totals': 'Offensive Totals',
        'off_per_game': "Offense Per Game",
        'def_totals': 'Defensive Totals',
        'def_per_game': 'Defense Per Game',
        'comb_totals': 'Combined Totals',
        'comb_per_game': 'Combined Per Game'
    }
    pretty_dict = ana_var_dict.update(num_dict)

    st.subheader("1. 2016 Warriors vs Cavaliers")
    wc, wc2 = st.columns([6,10])
    war_cav = ana_df.copy()
    war_cav = war_cav[(war_cav['season'] == 2016) & (war_cav['tm'].isin(['CLE', 'GSW']))]
    war_cav['team'] = war_cav['tm'].map({'CLE': 'Cavaliers', 'GSW': 'Warriors'})
    war_cav.loc[(war_cav['player'] == 'Anderson Varejão') & (war_cav['tm'] == 'CLE'), 'player'] = 'Anderson Varejão (Cavaliers)'
    war_cav.loc[(war_cav['player'] == 'Anderson Varejão') & (war_cav['tm'] == 'GSW'), 'player'] = 'Anderson Varejão (Warriors)'
    # st.write(war_cav)
    war_cav_2016 = px.bar(war_cav, x='player', y='per', color='team', text_auto=True, height=800, width=1000)
    war_cav_2016.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    war_cav_2016.update_xaxes(categoryorder='total descending', matches=None, showticklabels=True, tickangle=45)
    wc2.plotly_chart(war_cav_2016)

    # st.html("<hr style=\"height: 5px; background-color: red;\" />")

    # 2001 76ers vs Lakers
    st.subheader("2. 2001 76ers vs Lakers")
    six_lal = ana_df.copy()
    sl, sl2 = st.columns([6,10])
    six_lal = six_lal[(six_lal['season'] == 2001) & (six_lal['tm'].isin(['PHI', 'LAL']))]
    six_lal['team'] = six_lal['tm'].map({'PHI': '76ers', 'LAL': 'Lakers'})
    # st.write(six_lal)
    six_lal_2001 = px.bar(six_lal, x='player', y='per', color='team', text_auto=True, height=800, width=1000)
    six_lal_2001.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    six_lal_2001.update_xaxes(categoryorder='total descending', matches=None, showticklabels=True, tickangle=45)
    sl2.plotly_chart(six_lal_2001)

    #st.html("<hr style=\"height: 5px; background-color: red;\" />")

    # 2008 Celtics vs Lakers
    st.subheader("3. 2008 Celtics vs Lakers")
    cl_lal = ana_df.copy()
    cl, cl2 = st.columns([6,10])
    cl_lal = cl_lal[(cl_lal['season'] == 2008) & (cl_lal['tm'].isin(['BOS', 'LAL']))]
    cl_lal['team'] = cl_lal['tm'].map({'BOS': 'Celtics', 'LAL': 'Lakers'})
    # st.write(cl_lal)
    cl_lal_2008 = px.bar(cl_lal, x='player', y='per', color='team', text_auto=True, height=800, width=1000)
    cl_lal_2008.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    cl_lal_2008.update_xaxes(categoryorder='total descending', matches=None, showticklabels=True, tickangle=45)
    cl2.plotly_chart(cl_lal_2008)
    
    #st.html("<hr style=\"height: 5px; background-color: red;\" />")

    # 1984 Celtics vs Lakers
    st.subheader("4. 1984 Celtics vs Lakers")
    cl_lal2 = ana_df.copy()
    cl3, cl4 = st.columns([6,10])
    cl_lal2 = cl_lal2[(cl_lal2['season'] == 1984) & (cl_lal2['tm'].isin(['BOS', 'LAL']))]
    cl_lal2['team'] = cl_lal2['tm'].map({'BOS': 'Celtics', 'LAL': 'Lakers'})
    # st.write(cl_lal2)
    cl_lal_1984 = px.bar(cl_lal2, x='player', y='per', color='team', text_auto=True, height=800, width=1000)
    cl_lal_1984.update_traces(textposition='outside', texttemplate='<b>%{y:.2f}</b>')
    cl_lal_1984.update_xaxes(categoryorder='total descending', matches=None, showticklabels=True, tickangle=45)
    cl4.plotly_chart(cl_lal_1984)

    #st.html("<hr style=\"height: 5px; background-color: red;\" />")

# Conclusion
if s == "Conclusion":
    st.title("<b>THE FINAL Conclusion</b> for the NBA GOAT debate of this case study", unsafe_allow_html=True)
    st.markdown("We have analyzed the ten most popular NBA GOAT nominees, and the NBA Finals of some rivalry teams.")
    st.markdown("In the first analysis section, I feel that it is safe to say that the NBA GOAT is LeBron James.") # TODO: Add why LBJ is GOAT
    st.markdown("LeBron leads almost all the stats shown visually.")
    st.text("So, congratulations to LeBron James!", help='Also, Yay if you like LeBron, no boos if u prefer MJ or Kobe or any other player better! It always comes down to a personal choice!')
    st.markdown("And in the second part, we looked at some of the iconic championship seasons as well as some of the rivalry teams. (Including the long-lasting Lakers-Celtics Rivalry)")
    st.text("So, this marks the end of this project! I hope you enjoyed it! Thanks for reading!", help="Also, don't forget to star my Github repo!")


# Bibliography
if s == "Bibliography":
    st.title("Bibliography")
    st.text("[1]https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats/versions/40, DOA=2024/12/17", help='DOA (Date Of Access): Dec 17, 2024')
    st.caption("Near the end of the case study, I updated my dataset from version 31 to version 40, the newest by my DOA.")
    st.text("[2]NBA Math: https://www.nbamath.com")
    st.text("[3]HoopsHype: https://www.hoopshype.com")
    st.text("[4]ESPN: https://www.espn.com")
    st.text("[5]Sporting News: https://www.sportingnews.com")
