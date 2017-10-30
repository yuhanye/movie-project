
# load package -> library 
import pandas as pd # dataframe
import numpy as np
#%% read csv -> read_csv
actor = pd.read_csv('oscars-database.csv')
movie = pd.read_csv('movie-charac-wide-2015.csv')

# Award needed 
wkList = ['Actor', 'Actress','Actor in a Supporting Role', 'Actress in a Supporting Role',\
          'Actor in a Leading Role', 'Actress in a Leading Role']
#%%  split to list -> array
def split(x):
    return x.split(',')

movie['actorlist'] = movie.actors.apply(str).apply(split)

#%%
winner = np.zeros(len(movie))
nom = np.zeros(len(movie))
for i,imovie in enumerate(movie.actorlist.values):
    for j in imovie:
        winner[i] += len(actor.query('Name == @j and Winner== 1.0 and Award in @wkList')) # query,  subset (condition ):   subset(df, df$Award in @wklist)
        nom[i] += len(actor.query('Name == @j and Winner!= 1.0 and Award in @wkList'))
movie['winner'] = winner
movie['nomination'] = nom
     
    

#%%
movie.to_csv('./movie.csv')

#%% 
namelist = actor.query('Award in @wkList').Name.unique() 
#%%
from pytrends.request import TrendReq
pytrend = TrendReq()
res = [np.nan]*len(namelist)
for i,name in enumerate(namelist):
    try:
        pytrend.build_payload(kw_list=[name])
        interest_over_time_df = pytrend.interest_over_time()['2013':'2015']
        res[i] = interest_over_time_df[name].mean()
    except:
        print name

#%%
act = pd.DataFrame({'name':namelist,'meanScore':res})
act = act.set_index('name')
act.to_csv('./actorScore.csv')
