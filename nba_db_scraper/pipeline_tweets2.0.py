"""
This code creates a tweet extraction pipeline using the Twint tool. A previously generated csv file must
be provided for it. 

Author: PSC
"""

from create_databases import PATH_ROOT
import pandas as pd
import twint
import nest_asyncio
import datetime
import asyncio

def split_df(data: pd.DataFrame) -> list:
    """
    Splits DataFrame into smaller chunks
    """

    df_list = []
    size = len(data) / 1000
    i = 0 

    while i < len(data):
        df_list.append(data.loc[i:i+size].copy())
        i += size
    
    return df_list


async def twint_config(data: pd.DataFrame, twitter_data: pd.DataFrame) -> None:
    
    for i in range(len(data)): 
        # Configure
        c = twint.Config()
        c.Search = data.loc[i]['TEAM_NAME']
        c.Lang = 'en'
        c.Since = str(data.loc[i]['tweet_since'])
        c.Until = str(data.loc[i]['tweet_until'])
        c.Limit = 70
        c.Pandas = True
        c.Hide_output = True

        # Run
        await twint.run.Search(c)

        # Save
        results = twint.storage.panda.Tweets_df
        results['team'] = data.loc[i]['TEAM_NAME']
        results['game_id'] = data.loc[i]['GAME_ID']
        twitter_data = pd.concat([twitter_data, results[['tweet', 'team']]])

        # Monitor
        conclusion = format(i / len(data), ".4f")
        print('Conclusion: {}%'.format(conclusion))

        return twitter_data



async def main():
    nest_asyncio.apply()
    foundation = pd.read_csv(PATH_ROOT + 'foundation.csv')
    split_data = split_df(foundation)
    twitter_data = pd.DataFrame()
    tasks = [twint_config(split_data[i], twitter_data) for i in range(0,1000)]

    twitter_data = await asyncio.gather(
        *tasks
    )


    print('Saving File ...')
    twitter_data.to_csv(PATH_ROOT + 'twitter_data.csv')


if __name__ == '__main__':
    asyncio.run(main())
