# Imports
import streamlit as st
from streamlit_option_menu import option_menu as menu
st.set_page_config(layout="wide")
import numpy as np  # noqa: F401, E402
import plotly.express as px  # noqa: E402
import pandas as pd  # noqa: E402
pcq = px.colors.qualitative
pd.options.plotting.backend = "plotly"

my_path = ""

# Read in the dataset
player_totals = pd.read_csv(f"{my_path}\\Player Totals.csv")

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
NVar = ["season","pts","ast","fg","fga","ft","fta","g", 'fgm', 'ftm', 'ovr', 'age', 'x3p', 'x3pa', 'x2p', 'x2pa', 'pf', 'tov', 'per', 'ppg', 'rpg', 'orpg', 'drpg', 'apg', 'bpg', 'spg']
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
    '''
    Parameters:
    data_frame (`pd.DataFrame`)
    groupby_cols (`list` of `str` or `str`): The columns to groupby. (If nothing entered, default columns will be 'player' and 'ancient_pos')
    mode (`str`): Accepts 'sum' or 'mean'

    Returns:
    `pd.DataFrame`
    '''
    assert mode in ['sum', 'mean'], "`mode` must be one of 'sum' or 'mean'"
    cols = groupby_cols if groupby_cols is not None else ['player', 'ancient_pos']
    nvar = np.setdiff1d(NVar, cols)
    # print(cols)
    m = data_frame.copy()
    if mode == 'sum':
        return m.groupby(cols)[nvar].sum().reset_index()
    elif mode == 'mean':
        return m.groupby(cols)[nvar].mean().reset_index()
    # else:
    #     pass  # Optional TODO: add more

# Some tests
# df = agg(nba_graph, ['tm', 'ancient_pos', 'player'])
# print(df.columns)

# TEST
# graph_totals
# graph_totals.columns
# graph_totals.dtypes
# graph_avg

# Dictionaries
num_dict = {
    'season': 'Season',
    'pts': 'Points',
    'ast': 'Assists',
    'fg': 'Field Goals',
    'fga': 'Field Goals Attemps',
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
    'MIN':'Minnesoda Timberwolves',
    'MEM':'Memphis Grizzlies',
    "TOR":'Toronto Raptors',
    'NOP':"New Orleans Pelicans"
}
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
		options = ['Abstract', 'Background Information', 'Data Cleaning','Exploratory Analysis', 'Analysis of GOAT by stats for the ten most popular players', 'Analysis of the NBA Championship teams in iconic seasons', 'Conclusion', 'Bibliography'],
		menu_icon = 'stack',  # TODO: Change
		icons = ['bookmark-check', 'book', 'box', 'map', 'key-fill', 'list-check', 'star-fill', 'check2-circle'],  # TODO: Same as line 370
		default_index = 0,
		)


if s == "Abstract":
    st.title("NBA GOAT Decision")
    st.markdown("The debate over who holds the title of the Greatest of All Time (GOAT) in the NBA is one of the most spirited conversations among basketball enthusiasts. From legendary feats to iconic moments, various factors contribute to the greatness of players. However, when the chatter clears and emotions settle, it's the cold, hard stats that offer an objective lens through which we can attempt to settle this debate.")
    st.markdown("In this case study, we delve deep into the world of numbers to crown the NBA GOAT.<sup>2 3 4</sup> We'll explore an array of statistical categories, including scoring averages, assists, rebounds, and advanced metrics. By examining these figures, we aim to provide a comprehensive analysis that transcends personal bias and nostalgia.", unsafe_allow_html=True)
    st.markdown("Join us as we crunch the numbers, compare legends from different eras, and unveil who truly stands atop the NBA mountain based on their statistical dominance. Whether you're a fan of the flashy dunks, the clutch shots, or the all-around game, this case study promises to offer insights and revelations about the legends of the hardwood. Let's dive in and find out who the stats say is the ultimate GOAT!")
    st.markdown("This dataset is retrieved from kaggle <sup>1</sup>", unsafe_allow_html=True)

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
                - Scoring: Points per game (PPG), total points, and scoring titles.
                - Assists: Assists per game (APG), total assists, and assist titles.
                - Rebounds: Rebounds per game (RPG), total rebounds, and rebounding titles.
                - Advanced Metrics: An `ovr` (overall) score for each season based on the player's perfromances.
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
if s == "Exploratory Analysis":
    # Template:

    # st.subheader("A title")
    # col, col= st.columns([x,y])
    # # Remind: odd cols: input widgets; even cols: plotly plots
    # col.markdown("Description of what people can find using this")

    # with st.form("Whatever"):
    #    # Use input widgets... (Selectbox, checkbox, radio, multi-select, etc.)   
    #    submitted = st.form_submit_button("") 
    #    if submitted:
    #        fig = px.whatever_graph_type(**kwargs)
    #        # Whatever updates
    #        col.plotly_chart(fig)   

    # Key Numbering System:
    # Normal: from 1 to 999 or from 1601 to 999999 or from 1000010 to whatever
    # sliders: from 1000 to 1500
    # radio: from 1501 to 1550
    # Different multiselect choices basing on radio (or checkbox or whatever): from 1551 to 1600
    # Weird Keys: 1000000 to 1000009

    # Define some functions (and a list)
    tochoose = ["Team-Position", "Position-Team", "Player-Position", "Player-Team"]

    def a (graph_type: str) -> str:
        return f"Click to produce the {graph_type}."
    
    def b (a: str, b: str) -> str:
        return f"ChoiceError: Sorry, for the y-axis column corresponding to the x-axis column \"{a}\", we only support the \"{b}\" column."
    
    def err (msg: str, icon: str = None):
        '''
        Displays a streamlit error message, returns a `DeltaGenerator` object (`streamlit.error`)

        Parameters:
        msg (`str`): The error message you want to display using st.error;
        icon (`str`|`None`): The icon for the error message. Default is '🚨';

        Returns:
        `streamlit.error` (`DeltaGenerator`)
        '''
        Icon = "🚨" if not icon else icon
        return st.error(msg, icon=Icon)

    # Exploratory Analysis (Graphs)
    st.title("Exploratory Analysis")
    st.caption("This is where the fun part comes in :)")

    st.subheader("Box Plot to compare stats for players across different seasons")
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
    st.subheader("Box Plot to compare stats for players across different teams")
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
            st.write("Hmmm... Your keyboard seem's to have its own opinions... If this problem persists, please seek for professional help.")

      #######################################################################################################################################################################

    st.subheader("Visualization of stats across players")
    col7, col8 = st.columns([2,5])
    col7.markdown("In the histograms, you may find it hard to find some patterns. It'll be easier to find patterns in this scatter plot.") # TODO: Same as line 520
    col7.markdown("Compare stats between the scatter plot and the histograms below")

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
    st.subheader("Compare stats across players")
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
        bins = col5.slider("The amount of bins you want", 5, 35, step=1, key=1002) if usr_sel_bin_num else 10  # Might not work... we'll see
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        if submitted:
            df = agg(nba_graph)
            df = df[df['player'].isin(col5_player)]
            fig = px.histogram(df, col5_x, col5_y, color='player', histfunc=histfunc, histnorm=histnorm, barmode=barmode, nbins=bins, labels=all_dict, title="", log_y=logy, hover_data=['player', 'ancient_pos'])
            fig.update_traces(marker_line_width=1)
            col6.plotly_chart(fig)

    st.subheader("Histogram of comparing stats across different teams")
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

    #########################################################################################################################################################################
    
    st.subheader("Histogram for comparing a player's points/assists across his age")
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
        
    st.subheader("Compare avg stats across players")
    st.caption("We'll be using the average dataset for this one!")
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

    #####
    st.subheader("Compare avg stats across teams")
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
            # # Some TESTS during debugging
            # col11.write(x11)
            # col11.write(col11_team_input)
            # col11.write(col11_team)
            fig = px.histogram(x11, col11_x, col11_y, color='present_teams', histfunc=histfunc, histnorm=histnorm, barmode=barmode, nbins=bins, labels=all_dict.values(), title="", log_y=logy)
            fig.update_traces(marker_line_width=1)
            col12.plotly_chart(fig)

    ########################################################################################################################################################################
    st.subheader("Box Plot to compare stats for players across different seasons")
    col13, col14 = st.columns([2,5])

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
        boxmode = 'relative' if barmode_checkbox else 'group'
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
    st.subheader("Box Plot to compare stats for players across different teams")
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
            st.write("Hmmm... Your keyboard seem's to have its own opinions... If this problem persists, please seek for professional help.")

    #########################################################################################################################################################################
    st.subheader("Line plot for comparing stats across players")
    col15, col16 = st.columns([2,5])

    with st.form("Line"): # TODO: Sync with Line 749
        col15_x_input = col15.selectbox("Select a numeric column for the x-axis values", num_dict.values(), key=57)
        col15_y_input = col15.selectbox("Select a numeric column for the y-axis values", np.setdiff1d(list(num_dict.values()), col15_x_input), key=58)
        col15_player = col15.multiselect("Select some players", nba_75, max_selections=10, key=59)
        col15_x = [bname for bname, pname in num_dict.items() if pname == col15_x_input][0]
        col15_y = [bname for bname, pname in num_dict.items() if pname == col15_y_input][0]
        # Keys 60~63 are reserved
        logy = col15.checkbox("Do you want logy?", key=64)
        submitted = st.form_submit_button(a("Line Plot"))
        if submitted:
            df = agg(nba_graph)
            df = df[df['player'].isin(col15_player)]
            fig = px.line(df, col15_x, col15_y, color=col15_player, title=".", labels=all_dict.values(), log_y=logy)
            fig.update_traces(marker_line_width=1)
            col16.plotly_chart(fig)

    #########################################################################################################################################################################
    st.subheader("Sunburst Plot for comparing stats for teams and players")
    col17, col18 = st.columns([2,5])

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
        # Key 67 is reserved
        # col17_team = [bname for bname, pname in team_dict.items() if pname in col17_team_input]
        # col17_pos = [bname for bname, pname in pos_dict.items() if pname in col17_pos_input]
        bool_idx = (df1['tm'].isin(col17_team_input)) & (df1['ancient_pos'].isin(col17_pos_input))
        sppath = ['tm', 'ancient_pos', 'player']
        # elif choice == "Position-Team":  # Pos-Team
        #     df1 = agg(nba_graph, ['ancient_pos', 'tm'])
        #     col17_pos_input = col17.multiselect("select some positions:", pos_dict.values(), key=68)
        #     col17_team_input = col17.multiselect("Select some teams:", team_dict.values(), key=69, max_selections=10)
        #     # Key 70 is reserved
        #     col17_pos = [bname for bname,pname in pos_dict.items() if pname == col17_pos_input]
        #     col17_team = [bname for bname, pname in team_dict.items() if pname == col17_team_input]
        #     bool_idx = (df1['ancient_pos'].isin(col17_pos)) & (df1['tm'].isin(col17_team))
        #     sppath = ['ancient_pos', 'tm']
        # elif choice == "Player-Position":  # Player-Pos
        #     df1 = agg(nba_graph, ['player', 'ancient_pos'])
        #     col17_player = col17.multiselect("Select some players:", nba_75, key=71, max_selections=10)
        #     col17_pos_input = col17.multiselect("Select some positions:", pos_dict.values(), key=72)
        #     # Key 73 is reserved
        #     col17_pos = [bname for bname, pname in pos_dict.items() if pname == col17_pos_input]
        #     bool_idx = (df1['player'].isin(col17_player)) & (df1['ancient_pos'].isin(col17_pos))
        #     sppath = ['player', 'ancient_pos']
        # else:  # Player-Team
        #     df1 = agg(nba_graph, ['player', 'tm'])
        #     col17_player = col17.multiselect("Select some players:", nba_75, key=71, max_selections=10)
        #     col17_team_input = col17.multiselect("Select some teams:", team_dict.values(), key=72, max_selections=10)
        #     # Key 73 is reserved
        #     col17_team = [bname for bname, pname in team_dict.items() if pname == col17_team_input]
        #     bool_idx = (df1['player'].isin(col17_player)) & (df1['tm'].isin(col17_team))
        #     sppath = ['player', 'tm']
        submitted = st.form_submit_button(a("Sunburst Plot"))
        if submitted: 
            # # Some tests during debugging. There happens to be a major bug here.
            # st.dataframe(df1)
            # st.dataframe(df1[(df1['tm'].isin(col17_team)) & (df1['ancient_pos'].isin(col17_pos))])
            # st.write(bool_idx)
            # st.write(col17_team)
            # st.write(col17_pos)
            # st.write(col17_team_input)
            # st.write(col17_pos_input)
            fig1 = px.sunburst(df1[bool_idx], values = numcol, path=sppath, height=800, width=600)
            col18.plotly_chart(fig1)
            # elif choice == "Position-Team":
            #     fig = px.sunburst(df, col17_team, col17_pos)
            #     col18.plotly_chart(fig)
            # elif choice == "Player-Position":
            #     fig = px.sunburst(df, col17_player, col17_pos)
            #     col18.plotly_chart(fig)
            # else:
            #     fig = px.sunburst(df, col17_player, col17_team)
            #     col18.plotly_chart(fig)
        # Keys 74~96 are reserved

    # # Alternative option: Treemap
    # with st.form("Treemap"):
    #     choice = col17.selectbox("Select the columns you want to show in this graph: (Format: inner_circle-outer_circle)", tochoose, key=1602)
    #     if choice == tochoose[0]:
    #         col17_team_input = col17.multiselect("Select some teams:", team_dict.values(), key=74, max_selections=10)
    #         col17_pos_input = col17.multiselect("Select some positions:", pos_dict.values(), key=75)
    #         # Key 76 is reserved
    #         col17_team = [bname for bname, pname in team_dict.items() if pname == col17_team_input]
    #         col17_pos = [bname for bname, pname in pos_dict.items() if pname == col17_pos_input]
    #     elif choice == tochoose[1]:
    #         col17_pos_input = col17.multiselect("select some positions:", pos_dict.values(), key=77)
    #         col17_team_input = col17.multiselect("Select some teams:", team_dict.values(), key=78, max_selections=10)
    #         # Key 79 is reserved
    #         col17_pos = [bname for bname,pname in pos_dict.items() if pname == col17_pos_input]
    #         col17_team = [bname for bname, pname in team_dict.items() if pname == col17_team_input]
    #     elif choice == tochoose[2]:
    #         col17_player = col17.multiselect("Select some players:", nba_75, key=80, max_selections=10)
    #         col17_pos_input = col17.multiselect("Select some positions:", pos_dict.values(), key=81)
    #         # Key 82 is reserved
    #         col17_pos = [bname for bname, pname in pos_dict.items() if pname == col17_pos_input]
    #     else:
    #         col17_player = col17.multiselect("Select some players:", nba_75, key=83, max_selections=10)
    #         col17_team_input = col17.multiselect("Select some teams:", team_dict.values(), key=84, max_selections=10)
    #      # Key 73 is reserved
    #         col17_team = [bname for bname, pname in team_dict.items() if pname == col17_team_input]
    #     submitted = st.form_submit_button(a("Treemap"))
    #     if submitted:
    #         df = agg(nba_graph)
    #         if choice == tochoose[0]:
    #             fig = px.treemap(df, col17_team, col17_pos)
    #         elif choice == tochoose[1]:
    #             fig = px.treemap(df, col17_pos, col17_team)
    #             col18.plotly_chart(fig)
    #         elif choice == tochoose[2]:
    #             fig = px.treemap(df, col17_player, col17_pos)
    #             col18.plotly_chart(fig)
    #         else:
    #             fig = px.treemap(df, col17_player, col17_team)
    #             col18.plotly_chart(fig)

    #####
    st.subheader("Sunburst Plot for comparing stats for teams and seasons")
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

    #########################################################################################################################################################################
    # TODO: Change ALL to LINE PLOTS!
    st.subheader("Histogram for comparing a player's overall score across his age")
    col19, col20 = st.columns([2,5])

    with st.form("Hisotgram"):
        col19_player = col19.multiselect("Select some players:", nba_75, max_selections=10, key=97)
        # Keys 98 and 99 are reserved
        histnorm_checkbox = col19.checkbox("Click for a normalized histogram", key=100)
        barmode_checkbox = col19.checkbox("Click for a stack histogram chart", key=101)
        usr_sel_bin_num = col19.checkbox("Do you want to select the number of bins? (Default is 10)", key=102)
        logy = col19.checkbox("Do you want logy?", key=103)
        mean_or_sum = col19.checkbox("Click if you want `sum`, default `mean`", key=104)
        bins = col19.slider("The amount of bins you want", 5, 35, step=1, key=1007) if usr_sel_bin_num else 10  # Might not work... we'll see
        histnorm = 'percent' if histnorm_checkbox else None
        histfunc = 'avg' if not histnorm else None
        barmode = 'relative' if barmode_checkbox else 'group'
        submitted = st.form_submit_button(a("Histogram"))
        mean_sum = 'sum' if mean_or_sum else 'mean'
        if submitted:
            df = agg(nba_graph, ['age', 'player'], mean_sum)
            fig = px.histogram(df[df['player'].isin(col19_player)], 'age', 'ovr', 'player', histnorm=histnorm, histfunc=histfunc, barmode=barmode, nbins=bins, log_y=logy, title='·')
            fig.update_traces(marker_line_width=1)
            col20.plotly_chart(fig)

    #########################################################################################################################################################################


    #####

    st.subheader("Histogram for comparing a player's 2-pointers/3-pointers made across his age")
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

# Analysis
if s == "Analysis of GOAT by stats for the ten most popular players":
    st.title("Analysis of GOAT by stats for the ten most popular players")
    st.subheader("We'll be foucsing on the analysis for the ten most popular GOAT nominees: Lebron James, Michael Jordan, Kobe Bryant, Steph Curry and Magic Johnson, and")
    st.subheader("Larry Bird, Kareem Abdul-Jabbar, Tracy McGrady, Bill Russell and Wilt Chamberlain.")
    st.text("Note that because Bill Russell and Wilt Chamberlain are from the old days, their data are not included in the raw dataset.", help='Thanks')
    
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


    st.subheader("Analyzing Offensive stats:")
    st.markdown("We'll be looking at a facet plot with stats (per game also) first:")
    ac1, ac2 = st.columns([4,6])
    ac1.markdown("Here's the analysis for the ten players' offensive stats:")
    ac1.markdown("We can clearly see that LeBron leads both the Totals and the Per Game chart BY A LOT")
    ac1.markdown("Tracy McGrady is the last all two charts.")
    ac1.markdown("Interestingly, both of Jordan's score was less than Kobe. But he still ranked the 3rd")
    # af1 = go.Figure()
    # af1.add_trace(
    #     go.Bar(
    #         x=ana_df['player'], 
    #         y=ana_df['off_totals'], 
    #         name='Offensive Totals', 
    #         xaxis='x1', 
    #         yaxis='y1'
    #     )
    # )
    # af1.add_trace(
    #     go.Bar(
    #         x=ana_df['player'], 
    #         y=ana_df['off_per_game'], 
    #         xaxis='x2',
    #         yaxis='y2'
    #     )
    # )
    # af1.update_layout(
    #     title="Offensive Stats: Totals and Per Game", 
    #     xaxis=dict(domain=[0, 0.45]), 
    #     xaxis2=dict(domain=[0.55, 1]), 
    #     yaxis=dict(title='Total Points', range=[0,65000]), 
    #     yaxis2=dict(title='Points Per Game', range=[0,1000], anchor='x2'), 
    #     barmode='group', 
    #     showlegend=False, 
    #     height=400
    # )
    # af1.add_annotation(
    #     x=0.225, y=1.05, xref='paper', yref='paper', 
    #     text='Offensive Totals', 
    #     showarrow=False, 
    #     font=dict(size=14)
    # )
    # af1.add_annotation(
    #     x=0.775, y=1.05, xref='paper', yref='paper', 
    #     text='Offense Per Game', 
    #     showarrow=False, 
    #     font=dict(size=14)
    # )
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
    # st.write(ana_long.head())

    st.subheader("Analyzing Defensive stats:")
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
    ac3.markdown("Not surprisingly, Steph Curry is thje lowest of all. (I mean, reasonable, considering he's not so tall and bad at defense)")
    ac3.markdown("Also, MJ leads Kobe in Totals but got beaten by 2 in the Per Game")
    # af2 = px.bar(
    #     ana_long[ana_long['cat'] == 'Defensive'],
    #     'player',
    #     'value',
    #     'meas',
    #     facet_col='meas',
    #     title='Defensive Stats: Totals and Per Game',
    #     height=400
    # )
    # ac4.plotly_chart(af2)

    st.subheader("Analyzing All (combined) stats:")
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
    ac5.markdown("Kobe beats MJ and secured himself 2nd place")
    ac5.markdown("And here's the best part: Kareem beat MJ by 1.3k in the totals but lost to him by 19 in the Per Game (3rd, 4th decider)")
    # af3 = px.bar(
    #     ana_long[ana_long['cat'] == 'Combined'],
    #     'player',
    #     'value',
    #     'meas',
    #     facet_col='meas',
    #     title="Combined Stats: Totals and Per Game",
    #     height=400
    # )
    # ac6.plotly_chart(af3)

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

    st.write("As we can see, LeBron James leads the raw stats for points and assists, and Kareem (no doubt), leads in the Offensive Rebounds.")
    st.write("MJ leads the steals and Kareem leads the blocks and the Defensive Rebounds. (Reasonable, since he's the only center in this graph)")
    st.write("Overall (in this map), LeBron leads the offensive stats and Kareem leads the defensive stats (including offensive rebounds), with MJ a single lead in the steals.")
    st.write("T-Mac is still the worst in offensive stats but he is better than Steph Curry in the rebounds and defensive stats")

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

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # # with st.form("Analysis 2: PPG, APG, RPG vs players"):
    # ana_col3, ana_col4 = st.columns([4,5])
    # ana_col3.markdown("<b>In this graph, we are going to analyse the PPG (Points Per Game) and players</b>", unsafe_allow_html=True)
    # ana_fig2 = px.box(ana_df, 'player', 'ppg', points='all', labels=all_dict.values(), title="", hover_data=['player', 'season', 'per', 'ovr', 'apg', 'rpg'])
    # ana_fig2.update_traces(marker_line_width=1)
    # ana_col4.plotly_chart(ana_fig2)

    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("Again, the highest goes to Wilt, averaging over a stunning 50 pts in the 1962-63 NBA season.")
    # ana_col3.markdown("The highest medium goes to Wilt again, with 31.82297.")
    # ana_col3.markdown("Unsurprisingly, the lowest goes to T-Mac in his 2010-11 season (3.166667 ppg).")

    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("<hr>", unsafe_allow_html=True)

    # ana_col3.markdown("<i>Additionally, we are going to find the relationship between the APG and RPG against the players.</i>", unsafe_allow_html=True)
    # ana_fig3 = px.box(ana_df, 'player', 'apg', points='all', labels=all_dict.values(), title="", hover_data=['player', 'season', 'ovr', 'per'])
    # ana_fig3.update_traces(marker_line_width=1)
    # ana_col4.plotly_chart(ana_fig3)

    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("Not surprisingly, Magic Johnson leads the highest APG (and the highest medium) by 13.0597 and 11.91667 respectively.")
    # ana_col3.markdown("And shockingly, the highest APG for Kobe Bryant (6.333) is smaller than that of Magic Johnson's lowest (6.875).")
    # ana_col3.markdown("And unsurprisingly, the lowest APG goes to Tracy in (yep, you've guessed it, 2010-11 season), only avg 1 assists per game!")

    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")
    # ana_col3.markdown("<hr>", unsafe_allow_html=True)

    # ana_col3.markdown("<i>And in this graph, we explore RPG against players</i>", unsafe_allow_html=True)
    # ana_fig4 = px.box(ana_df, 'player', 'rpg', points='all', labels=all_dict.values(), title="", hover_data=['player', 'season', 'ovr', 'per', 'ppg'])
    # ana_fig4.update_traces(marker_line_width=1)
    # ana_col4.plotly_chart(ana_fig4)

    # ana_col3.markdown("\n")
    # ana_col3.markdown("\n")    
    # ana_col3.markdown("We all know that Wilt and Bill are MONSTERS at rebounds, it seems that Wilt narrowly beats Bill. But we're not going to look at them for now.")
    # ana_col3.markdown("Surprisingly, Magic Johnson also leads the highest RPG (9.268205), and that is in the 1982-1983 NBA season.")
    # ana_col3.markdown("The highest medium goes to LBJ, with a 7.688889.")
    # ana_col3.markdown("And another point worth noting: although Kobe is still the lowest on RPG (1.859155), Stephen Curry's RPG medium is actually about 0.4 lower than that of Kobe's.")

    # st.markdown("<hr style=\"height: 5px; background-color: red;\" />", unsafe_allow_html=True)

    # # with st.form("Analysis 1: PER vs players"):
    # ana_col1, ana_col2 = st.columns([4,5])
    # ana_col1.markdown("<b>In this graph, we are going to analyse the PER (Player Efficiency Ratings) and players</b>", unsafe_allow_html=True)
    # ana_fig1 = px.box(ana_df, 'player', 'per', points='all', labels=all_dict.values(), title="", hover_data=['player', 'season', 'per', 'ovr'])
    # ana_fig1.update_traces(marker_line_width=1)
    # ana_col2.plotly_chart(ana_fig1)

    # ana_col1.markdown("\n")
    # ana_col1.markdown("\n")
    # ana_col1.markdown("From the chart, we can clearly see that MJ holds the most PER in a season (40.5679), in the 1989-1990 NBA season.")
    # ana_col1.markdown("Surprisingly, the highest PER medium goes to Magic Johnson, with a 33.24051, narrowly beating LBJ and Michael.")
    # ana_col1.markdown("The lowest PER in a season goes to T-Mac, with a 3 in the 2010 season.")

    # st.markdown("<hr style=\"height: 5px; background-color: red;\" />", unsafe_allow_html=True)

    # # with st.form("Anaysis 3: Seasons-played vs PER/OVR corr"):
    # ana_col5, ana_col6 = st.columns([4,5])
    # ana_fig5 = px.histogram(ana_corr_df, 'Player Name', 'Correlation', color='Player Name', text_auto='.2f', title="Correlation of PER (Player Efficiency Ratings) and OVR (Overall)")
    # ana_fig5.update_traces(marker_line_width=1, textposition='outside')
    # ana_col6.plotly_chart(ana_fig5)
    
    # ana_col5.markdown("\n")
    # ana_col5.markdown("\n")
    # ana_col5.markdown("We can see that Tracy leads this by 0.958, followed by Larry's 0.929.")
    # ana_col5.markdown("These players' Player Efficiency Ratings are highly correlated to their overall.")
    # ana_col5.markdown("You may recall earlier (In the Data Cleaning section) how i did the overall calculations.")
    # ana_col5.markdown("NOTE: There are no stats for Wilt and Bill because some stats weren't being recorded at that time.")
    # ana_col5.markdown("\n")
    # ana_col5.markdown("\n")
    # ana_col5.markdown("\n")
    # ana_col5.markdown("\n")
    # ana_col5.markdown("\n")
    # ana_col5.markdown("\n")
    # ana_col5.markdown("\n")
    # ana_col5.markdown("\n")
    
    st.markdown("<hr style=\"height: 5px; background-color: red;\" />", unsafe_allow_html=True)
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    st.text("From that, I think it's safe to say that LeBron James is the NBA GOAT in this analysis section.", help="Although, any disagreement is welcomed. But feel free to go look at the graphs yourselves!")

if s == "Analysis of the NBA Championship teams in iconic seasons":
    st.title("Analysis of the NBA Championship teams in iconic seasons (eg: 1995 Bulls, 1986 Celtics, etc.)")

# Conclusion
if s == "Conclusion":
    st.title("Conclusion for the NBA GOAT debate")




# Bibliography
if s == "Bibliography":
    st.title("Bibliography")
    st.text("[1]https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats/versions/31")
    st.text("[2]NBA Math: nbamath.com")
    st.text("[3]HoopsHype: hoopshype.com")
    st.text("[4]ESPN: espn.com")
    st.text("[5]Sporting News: sportingnews.com")
