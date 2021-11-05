import pandas as pd 
from datetime import datetime
from time import sleep

def redoBase(date_num):
    base_final = f'https://www.espn.com/mens-college-basketball/schedule/_/date/{date_num}/group/50'
    return base_final

def initialDF(date_num):
    base_final = redoBase(date_num)
    novDF = pd.read_html(base_final)[0]
    novDF['Date'] = processDate(date_num)
    novDF.drop(columns=['time'],inplace=True)
    novDF.drop(columns=['nat tv'],inplace=True)
    novDF.drop(columns=['tickets'],inplace=True)
    novDF.drop(columns=['location'],inplace=True)
    novDF.drop(columns=['Unnamed: 6'],inplace=True)
    date_num += 1
    sleep(5)
    return novDF, date_num

def repeatDF(novDF,date_num,final_num):
    while date_num <= final_num:
        if date_num != 20211224 or date_num != 20211226:
            base_final = redoBase(date_num)
            try:
                my_df = pd.read_html(base_final)[0]
                my_df['Date'] = processDate(date_num)
                my_df.drop(columns=['time'],inplace=True)
                my_df.drop(columns=['nat tv'],inplace=True)
                my_df.drop(columns=['tickets'],inplace=True)
                my_df.drop(columns=['location'],inplace=True)
                my_df.drop(columns=['Unnamed: 6'],inplace=True)
                novDF = novDF.append(my_df)
                date_num += 1
                sleep(5)
            except Exception as e:
                print(e)
                date_num += 1
                sleep(5)
        else:
            date_num += 1
    return novDF

def processDate(date_num):
    date_num = str(date_num)
    year = date_num[0:4]
    month = date_num[4:6]
    day = date_num[6:8]
    return f'{month}-{day}-{year}'

def getNov():
    date_num = 20211109
    final_num = 20211130
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    sleep(10)
    return novDF

def getDec():
    date_num = 20211201
    20211224
    20211226
    final_num = 20211231
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    sleep(10)
    return novDF

def getJan():
    date_num = 20220101
    final_num = 20220131
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    sleep(10)
    return novDF

def getFeb():
    date_num = 20220201
    final_num = 20220228
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    sleep(10)
    return novDF

def getMar():
    date_num = 20220301
    final_num = 20220306
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    sleep(10)
    return novDF    

def cleanup(df):
    df = df.rename(columns={'matchup':'Away','Unnamed: 1':'Home'})
    df['Away'] = df['Away'].map(lambda x: removeRankings(x))
    df['Home'] = df['Home'].map(lambda x: removeRankings(x))
    return df

def removeRankings(x):
    slen = len(x.split())
    if x.startswith('#'):
        x = x.lstrip(f'{x.split()[0]} ')
        slen -= 1
        x = ' '.join(x.split()[0:slen-1])
        return x
    else:
        x = ' '.join(x.split()[0:slen-1])
        return x


def main():
    startTime = datetime.now()
    print('Starting!')
    mainDF = getNov()
    print('November is done')
    print(datetime.now() - startTime)
    mainDF = mainDF.append(getDec())
    print('December is done')
    print(datetime.now() - startTime)
    mainDF = mainDF.append(getJan())
    print('Janurary is done')
    print(datetime.now() - startTime)
    mainDF = mainDF.append(getFeb())
    print('February is done')
    print(datetime.now() - startTime)
    mainDF = mainDF.append(getMar())
    print('March is done')
    print(datetime.now() - startTime)
    mainDF = cleanup(mainDF)
    mainDF.to_csv('NCAA2021-22_Final.csv',index=False)
    print(datetime.now() - startTime)
    print('Done!')

main()