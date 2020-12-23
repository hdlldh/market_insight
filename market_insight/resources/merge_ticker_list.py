import pandas as pd
from collections import defaultdict
file_date = '12-23-2020'

WatchFile = "./watch_list.csv"
DowCompFile = f"dow-jones-indices-{file_date}.csv"
NasdaqFile = f"nasdaq-composite-index-{file_date}.csv"
Russel1KFile = f"russell-1000-index-{file_date}.csv"
SP400File = f"sp-400-index-{file_date}.csv"
SP500File = f"sp-500-index-{file_date}.csv"

cols = ['Symbol', 'Name']
WatchList = pd.read_csv(WatchFile, index_col='Symbol', usecols=cols)
WatchList['WatchList'] = 1
DowComp = pd.read_csv(DowCompFile, index_col='Symbol', usecols=cols, skipfooter=1, engine='python')
DowComp['DowComposite'] = 1
Nasdaq = pd.read_csv(NasdaqFile, index_col='Symbol', usecols=cols, skipfooter=1, engine='python')
Nasdaq['NasdaqComposite'] = 1
Russel1K = pd.read_csv(Russel1KFile, index_col='Symbol', usecols=cols, skipfooter=1, engine='python')
Russel1K['Russel1K'] = 1
SP400 = pd.read_csv(SP400File, index_col='Symbol', usecols=cols, skipfooter=1, engine='python')
SP400['S&P400'] = 1
SP500 = pd.read_csv(SP500File, index_col='Symbol', usecols=cols, skipfooter=1, engine='python')
SP500['S&P500'] = 1

out = defaultdict(dict)
# for df in [WatchList, DowComp]:
for df in [WatchList, DowComp, Nasdaq, Russel1K, SP400, SP500]:
    df_dict = df.to_dict("index")
    for key, val in df_dict.items():
        out[key].update(val)

out_df = pd.DataFrame.from_dict(out, "index")
out_df.index.name = 'Symbol'
out_df = out_df.reset_index()
out_df.sort_values('Symbol', inplace=True)
out_df.to_csv('symbol_list.csv', index=False)
