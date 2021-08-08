"""
This code was created based on an article written by John Mannelly.
It connects to stats.nba.com and extracts specific databases contained in the website 

Full article:
https://jman4190.medium.com/building-an-nba-mysql-database-with-python-c653fa15333c
"""

import requests
import pandas as pd
#import pandas_gbq
#from google.oauth2 import service_account

PATH_ROOT = R'C:\Users\PerdoCaiafa\NBA_Proj\\'

def export_to_gbq(df, table_name):
    credentials= service_account.Credentials.from_service_account_file(r'C:\Users\PerdoCaiafa\Documents\MAUA\MINOR'
                                                                       r'\PROJETOS\NBA Project-65d01c29a337.json')
    pandas_gbq.context.credentials= credentials
    pandas_gbq.context.project= 'nba-project-310316'
    pandas_gbq.to_gbq(df, table_name, project_id='nba-project-310316')

def create_games_dataset():
    headers  = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    season_list = [
        '1996-97',
        '1997-98',
        '1998-99',
        '1999-00',
        '2000-01',
        '2001-02',
        '2002-03',
        '2003-04',
        '2004-05',
        '2005-06',
        '2006-07',
        '2007-08',
        '2008-09',
        '2009-10',
        '2010-11',
        '2011-12',
        '2012-13',
        '2013-14',
        '2014-15',
        '2015-16',
        '2016-17',
        '2017-18',
        '2018-19',
        '2019-20',
        '2020-21'
    ]
    #Opções de per_mode -> PerGame ; Per100Possessions ; Per36
    per_mode = 'Totals'

    #Download de estatísticas de jogadores
    print('Acessando servidores da NBA....')
    #inicializa lista para onde os dados vão
    game_info= list()
    # loop para ler todas as temporadas
    for season_id in season_list:
        print("Baixando temporada "+season_id)
        # url para scrape
        game_info_url = 'https://stats.nba.com/stats/teamgamelogs?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=' + season_id + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&VsConference=&VsDivision='
        # json response
        response = requests.get(url=game_info_url, headers=headers, timeout= 60).json()
        # puxando só dados necessários
        game_info.append(response['resultSets'][0]['rowSet'])

    #resultado dos requests é uma lista de listas. É necessário 'achatar' a lista
    game_info_flat= [item for sublist in game_info for item in sublist]
    game_info_df=pd.DataFrame(game_info_flat)
    game_info_df= game_info_df.rename(columns= {
        0: "SEASON_YEAR",
        1: "TEAM_ID",
        2: "TEAM_ABBREVIATION",
        3: "TEAM_NAME",
        4: "GAME_ID",
        5: "GAME_DATE",
        6: "MATCHUP",
        7: "WL",
        8: "MIN",
        9: "FGM",
        10: "FGA",
        11: "FG_PCT",
        12: "FG3M",
        13: "FG3A",
        14: "FG3_PCT",
        15: "FTM",
        16: "FTA",
        17: "FT_PCT",
        18: "OREB",
        19: "DREB",
        20: "REB",
        21: "AST",
        22: "TOV",
        23: "STL",
        24: "BLK",
        25: "BLKA",
        26: "PF",
        27: "PFD",
        28: "PTS",
        29: "PLUS_MINUS",
        30: "GP_RANK",
        31: "W_RANK",
        32: "L_RANK",
        33: "W_PCT_RANK",
        34: "MIN_RANK",
        35: "FGM_RANK",
        36: "FGA_RANK",
        37: "FG_PCT_RANK",
        38: "FG3M_RANK",
        39: "FG3A_RANK",
        40: "FG3_PCT_RANK",
        41: "FTM_RANK",
        42: "FTA_RANK",
        43: "FT_PCT_RANK",
        44: "OREB_RANK",
        45: "DREB_RANK",
        46: "REB_RANK",
        47: "AST_RANK",
        48: "TOV_RANK",
        49: "STL_RANK",
        50: "BLK_RANK",
        51: "BLKA_RANK",
        52: "PF_RANK",
        53: "PFD_RANK",
        54: "PTS_RANK",
        55: "PLUS_MINUS_RANK",

    })

    return game_info_df


def main():
    #print('Exportando dados para o BigQuery....')
    #export_to_gbq(game_info_df, 'NBA_Test1.nba_game_results')
    data = create_games_dataset()
    print('Salvando localmente....')
    data.to_csv(PATH_ROOT + 'game_info.csv')


if __name__ == '__main__':
    main()
