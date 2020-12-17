import pandas as pd

DowCompFile = './DowComposite.csv'
NasdaqFile = './Nasdaq100.csv'
R1000File = './Russell1000.csv' 
R2000File = './Russell2000.csv'
SP100File = './SP100.csv'
SP400File = './SP400.csv'
SP500File = './SP500.csv'
SP600File = './SP600.csv'
WatchFile = './watch_list.csv'

DowCompData = pd.read_csv(DowCompFile)
#print DowCompData.head()
NasdaqData = pd.read_csv(NasdaqFile)
#print NasdaqData.head()
R1000Data = pd.read_csv(R1000File)
#print R1000Data.head()
R2000Data = pd.read_csv(R2000File)
#print R2000Data.head()
SP100Data = pd.read_csv(SP100File)
#print SP100Data.head()
SP400Data = pd.read_csv(SP400File)
#print SP400Data.head()
SP500Data = pd.read_csv(SP500File)
#print SP500Data.head()
SP600Data = pd.read_csv(SP600File)
#print SP500Data.head()
WatchData = pd.read_csv(WatchFile)

MergeData = pd.concat([DowCompData,NasdaqData,R1000Data,R2000Data,\
    SP100Data,SP400Data,SP500Data,SP600Data,WatchData]).drop_duplicates()

MergeData['DowComposite'] = 0
MergeData['Nasdaq100'] = 0
MergeData['Russell1000'] = 0
MergeData['Russell2000'] = 0
MergeData['S&P100'] = 0
MergeData['S&P500'] = 0
MergeData['S&P400'] = 0
MergeData['S&P600'] = 0
MergeData['WatchList'] = 0

MergeData.loc[MergeData['Symbol'].isin(DowCompData['Symbol']),'DowComposite'] = 1
MergeData.loc[MergeData['Symbol'].isin(NasdaqData['Symbol']),'Nasdaq100'] = 1
MergeData.loc[MergeData['Symbol'].isin(R1000Data['Symbol']),'Russell1000'] = 1
MergeData.loc[MergeData['Symbol'].isin(R2000Data['Symbol']),'Russell2000'] = 1
MergeData.loc[MergeData['Symbol'].isin(SP100Data['Symbol']),'S&P100'] = 1
MergeData.loc[MergeData['Symbol'].isin(SP500Data['Symbol']),'S&P500'] = 1
MergeData.loc[MergeData['Symbol'].isin(SP400Data['Symbol']),'S&P400'] = 1
MergeData.loc[MergeData['Symbol'].isin(SP600Data['Symbol']),'S&P600'] = 1
MergeData.loc[MergeData['Symbol'].isin(WatchData['Symbol']),'WatchList'] = 1

MergeData.sort_values('Symbol',inplace=True)
MergeData.to_csv('symbol_list.csv',index=False)

#print len(MergeData)
#print len(set(list(MergeData['Symbol'])))
