import pandas as pd 
from datetime import datetime
from time import sleep

def appendThisYear(mmdd):
    yyyy = datetime.now().year
    yyyy = str(yyyy)
    yyyymmdd = yyyy + mmdd
    return int(yyyymmdd)

def appendNextYear(mmdd):
    yyyy = datetime.now().year
    yyyy += 1
    yyyy = str(yyyy)
    yyyymmdd = yyyy + mmdd
    return int(yyyymmdd)

def redoBase(date_num):
    base_final = f'https://www.espn.com/mens-college-basketball/schedule/_/date/{date_num}/group/50'
    return base_final

def initialDF(date_num):
    base_final = redoBase(date_num)
    novDF = pd.read_html(base_final)[0]
    novDF['Date'] = processDate(date_num)
    novDF.drop(columns=['TIME'],inplace=True)
    novDF.drop(columns=['TV'],inplace=True)
    novDF.drop(columns=['tickets'],inplace=True)
    novDF.drop(columns=['location'],inplace=True)
    date_num += 1
    return novDF, date_num

def repeatDF(novDF,date_num,final_num):
    while date_num <= final_num:
        if date_num != 20241224 or date_num != 20241226:
            base_final = redoBase(date_num)
            try:
                my_df = pd.read_html(base_final)[0]
                my_df['Date'] = processDate(date_num)
                my_df.drop(columns=['TIME'],inplace=True)
                my_df.drop(columns=['TV'],inplace=True)
                my_df.drop(columns=['tickets'],inplace=True)
                my_df.drop(columns=['location'],inplace=True)
                novDF = pd.concat([novDF,my_df])
                date_num += 1
                sleep(1)
            except Exception as e:
                print(e)
                date_num += 1
                sleep(1)
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
    date_num = appendThisYear('1109')
    final_num = appendThisYear('1130')
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    return novDF

def getDec():
    date_num = appendThisYear('1201')
    final_num = appendThisYear('1231')
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    return novDF

def getJan():
    date_num = appendNextYear('0101')
    final_num = appendNextYear('0131')
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    return novDF

def getFeb():
    date_num = appendNextYear('0201')
    final_num = appendNextYear('0228')
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    return novDF

def getMar():
    date_num = appendNextYear('0301')
    final_num = appendNextYear('0306')
    novDF, date_num = initialDF(date_num)
    novDF = repeatDF(novDF,date_num,final_num)
    return novDF    

def cleanup(df):
    df = df.rename(columns={'MATCHUP':'Away','MATCHUP.1':'Home'})
    df['Home'] = df['Home'].apply(lambda x: removeAtSign(x))
    df['Away'] = df['Away'].apply(lambda x: removeRankings(x))
    df['Home'] = df['Home'].apply(lambda x: removeRankings(x))
    return df

def removeRankings(x):
    l = x.split(' ')
    if l[0].isdigit():
        del l[0]
        return ' '.join(l)
    return x

def removeAtSign(x):
    return x[2:]


def main():
    startTime = datetime.now()
    print('Starting!')
    mainDF = getNov()
    print('November is done')
    print(datetime.now() - startTime)
    mainDF = pd.concat([mainDF,getDec()])
    print('December is done')
    print(datetime.now() - startTime)
    mainDF = pd.concat([mainDF,getJan()])
    print('Janurary is done')
    print(datetime.now() - startTime)
    mainDF = pd.concat([mainDF,getFeb()])
    print('February is done')
    print(datetime.now() - startTime)
    mainDF = pd.concat([mainDF,getMar()])
    print('March is done')
    print(datetime.now() - startTime)
    mainDF = cleanup(mainDF)
    mainDF.to_csv('NCAA2024-25_Final.csv',index=False)
    print(datetime.now() - startTime)
    print('Done!')

main()