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

def main():
    nest_asyncio.apply()
    foundation = pd.read_csv(PATH_ROOT + 'foundation.csv')
    twitter_data = pd.DataFrame()

    for i in range(len(foundation)):
        # Configure
        c = twint.Config()
        c.Search = foundation.loc[i]['TEAM_NAME']
        c.Lang = 'en'
        c.Since = str(foundation.loc[i]['tweet_since'])
        c.Until = str(foundation.loc[i]['tweet_until'])
        c.Limit = 70
        c.Pandas = True
        c.Hide_output = True

        # Run
        twint.run.Search(c)

        # Save 
        results = twint.storage.panda.Tweets_df
        results['team'] = foundation.loc[i]['TEAM_NAME']
        results['game_id'] = foundation.loc[i]['GAME_ID']
        twitter_data = pd.concat([twitter_data, results[['tweet', 'team']]])
        conclusion = format(i / len(foundation), ".4f")
        print('Conclusion: {}%'.format(conclusion))

    print('Saving File ...')
    twitter_data.to_csv(PATH_ROOT + 'twitter_data.csv')


if __name__ == '__main__':
    main()
