import time
import pandas as pd
import os
import Dividend as dv
import Earnings as er
import Splits as sp   
import GoogleCalendar as gc
import EventCreation as ec
import numpy as np
import random
from apiclient.discovery import build
def main():

    tickers_list = pd.read_csv('./Inputs/TickerList.csv')
    Info = pd.read_csv('./Inputs/Info.csv')
    sleep = int(Info['Data'][1])
    randsleep = int(Info['Data'][2])
    tickers_len = len(tickers_list)

    Info = pd.read_csv('./Inputs/Info.csv')
    Calendar_Title = Info['Data'][0].strip()
    print(Calendar_Title)
    calendar_id,creds = gc.main()
    service = build("calendar", "v3",credentials= creds)

    poly_div = []
    poly_split = []
    nasdaq_div = []
    nasdaq_earn = []
    nasdaq_split = []
    yahoo_earn = []
    alpha_div = []
    finviz_earn = []
    marketbeat_split = []

    polycount = 0
    yahoocount = 0
    scrapecount = 0
    nascount = 0
    count = 0
    startTime = time.time()
    #Polygon was a little odd, so it needed an extra timer  
    p1, p2, n1,n2,n3,y1,s = -65,-65,-65,-65,-65,-65,-65,
    pstop,nstop,ystop,sstop,mbstop,fstop = 0,0,0,0,0,0
    while(count < 9):
        prev_poly = polycount
        for i in range(5):
            if(polycount == tickers_len):
                polycount = 0
            ticker = tickers_list['Ticker'][polycount]

            if(len(poly_div) != tickers_len and time.time()-p1 >= 60):
                date = dv.polyio_div(ticker)                
                poly_div.append(date)
                polycount += 1 
            elif(len(poly_split) != tickers_len and time.time()-p2 >= 60 and len(poly_div) == tickers_len):
                date = sp.polyio_split(ticker)                
                poly_split.append(date)
                polycount += 1                
            elif(len(poly_split) == tickers_len and pstop == 0):
                count += 2
                pstop =1
        if(prev_poly != polycount or tickers_len <= 4):
            p1 = time.time()
            p2 = time.time()
        for i in range(1):
            if(nascount == tickers_len):
                nascount = 0
            ticker = tickers_list['Ticker'][nascount]
            if(len(nasdaq_div) != tickers_len and time.time()-n1 >= 40 + (random.random() * 5)):
                date = dv.nasdaq_div(ticker)
                nasdaq_div.append(date)
                nascount += 1
                n1=time.time()
            elif(len(nasdaq_earn) != tickers_len and time.time()-n2 >= 40 + (random.random() * 7) and len(nasdaq_div) == tickers_len):
                date = er.nasdaq_earn(ticker)
                nasdaq_earn.append(date)
                nascount += 1
                n2=time.time()                                                
            elif(len(nasdaq_split) != tickers_len and time.time()-n3 >= 40 + (random.random() * 4) and len(nasdaq_earn) == tickers_len ):
                split_dates = sp.nasdaq_split(tickers_list)  
                print("nasdaq", split_dates)              
                nasdaq_split = split_dates
                nascount += 1
                n3=time.time()
            elif(len(nasdaq_earn) == tickers_len and nstop == 0 and len(nasdaq_split) == tickers_len ):
                count += 3
                nstop = 1
        for i in range(5):
            if(yahoocount == tickers_len):
                yahoocount = 0
            ticker = tickers_list['Ticker'][yahoocount]
            if(len(yahoo_earn) != tickers_len and time.time()-y1 >= 30):
                date = er.yahoo_earn(ticker)
                yahoo_earn.append(date)
                yahoocount += 1
                y1 = time.time()
            elif(len(yahoo_earn) == tickers_len and ystop == 0):
                count += 1
                ystop = 1
        for i  in range(1):
            if(scrapecount == tickers_len):
                scrapecount = 0     
            ticker = tickers_list['Ticker'][scrapecount]
            if(len(finviz_earn) != tickers_len and time.time()-s >= 40+ (random.random() * 3)):
                date =er.finviz_earn(ticker)
                finviz_earn.append(date)
            elif(len(finviz_earn) == tickers_len and fstop == 0 ):
                count += 1
                fstop = 1
            if(len(alpha_div) != tickers_len and time.time()-s >= 45+ (random.random() * 3)):
                date = dv.alpha_div(ticker)
                alpha_div.append(date)
                scrapecount += 1
            elif(len(alpha_div) == tickers_len and sstop == 0  ):
                count += 1
                sstop = 1
            if(len(marketbeat_split) != tickers_len and time.time()-s >= 45 + (random.random() * 4)):
                split_dates = sp.marketbeat_split(tickers_list)
                print("Marketbeat", split_dates)
                marketbeat_split = split_dates                
                s = time.time()
            elif(len(marketbeat_split) == tickers_len and mbstop == 0  ) :                
                count+=1
                mbstop = 1
        pb1 = startTime
        nb2 = startTime
        nb3 = startTime
        if(p2 > 0):
            pb2 = p2
        if(n2 > 0):
            nb2 = n2
        if(n3 > 0):
            nb3 = n3
                
        print("Waiting | Time since start for Polygon: ","Dividends:",round((p1- startTime),2),"Splits",round((pb2-startTime),2))
        print("Waiting | Time since start for  NasDaq","Dividends:", round((n1-startTime),2),"Earnings:", round((nb2-startTime),2),
        "Splits:",round((nb3- startTime),2))
        print("Waiting | Time since start for seeking yahoo: ","Earnings:", round((y1-startTime),2))
        print("Waiting | Time since start for seeking alpha, finviz, and marketbeat: ",round((s-startTime),2))
        print("Number of finished ones:", count ,"Total Number of Tickers:",tickers_len ) 
        if(count != 9 ):
            sleep_add = round((random.random() * randsleep),2)
            print(f"Waiting for {round(sleep + sleep_add,2)} seconds now")
            time.sleep(sleep + sleep_add )
            "Finishd=ed"
                  
        
    total_div = []
    total_earn= []
    total_split = []
    
    for i in range(tickers_len):
        ticker = tickers_list['Ticker'][i]
        entry = [ticker,poly_div[i],nasdaq_div[i],alpha_div[i]]
        total_div.append(entry)
    for i in range(tickers_len):
        ticker = tickers_list['Ticker'][i]
        entry = [ticker,nasdaq_earn[i],yahoo_earn[i],finviz_earn[i]]
        total_earn.append(entry)
    for i in range(tickers_len):
        ticker = tickers_list['Ticker'][i]
        entry = [ticker,poly_split[i],nasdaq_split[i],marketbeat_split[i]]
        total_split.append(entry)
        
    
    fail = 0
    fail2 = 0    
    for i in range(len(total_div)):
        fail = 0
        fail2 = 0
        event, fail = ec.createDivEvent(total_div[i][0],service,total_div[i][1],total_div[i][2],total_div[i][3])
        if(fail != 1):
            ticker = total_div[i][0]
            polygon = total_div[i][1]
            nasdaq = total_div[i][2]
            alpha = total_div[i][3]
            result = service.events().list(calendarId =calendar_id ).execute()
            for i  in range(len(result['items'])):
               
                descrp = result['items'][i]['description']
                summary = result['items'][i]['summary']
                descrp = descrp.strip()
                summary = summary.strip()
                guess_descrip = f'Polygon.IO: {polygon} | Nasdaq: {nasdaq} | Seeking Alpha: {alpha}'
                guess_descrip =guess_descrip.strip()
                guess_summary = f'{ticker} has an ex-dividend date today'
                guess_summary =guess_summary.strip()

                if(descrp == guess_descrip):
                    
                    fail2 = 1  
            if(fail2 != 1):
                service.events().insert(calendarId=calendar_id, body=event).execute()

    for i in range(len(total_earn)):
        fail = 0
        fail2 = 0
        event, fail = ec.createEarnEvent(total_earn[i][0],service,total_earn[i][1],total_earn[i][2],total_earn[i][3])
        if(fail != 1):
            ticker = total_div[i][0]
            nasdaq = total_earn[i][1]
            yahoo = total_earn[i][2]
            finviz = total_earn[i][3]
            result = service.events().list(calendarId =calendar_id ).execute()
            for i  in range(len(result['items'])):
               
                descrp = result['items'][i]['description']
                summary = result['items'][i]['summary']
                descrp = descrp.strip()
                summary = summary.strip()
                guess_descrip = f'Nasdaq: {nasdaq} |  Yahoo: {yahoo} | Finviz: {finviz}'
                guess_descrip =guess_descrip.strip()
                guess_summary = f'{ticker} has earnings today'
                guess_summary =guess_summary.strip()
                
                if(descrp == guess_descrip):                    
                    fail2 = 1  
            if(fail2 != 1):
                service.events().insert(calendarId=calendar_id, body=event).execute()
    for i in range(len(total_split)):
        fail = 0
        fail2 = 0
        event, fail = ec.createSplitEvent(total_split[i][0],service,total_split[i][1],total_split[i][2],total_split[i][3])
        if(fail != 1):
            ticker = total_div[i][0]
            polygon = total_split[i][1]
            nasdaq = total_split[i][2]
            mbeat = total_split[i][3]
            result = service.events().list(calendarId =calendar_id ).execute()
            for i  in range(len(result['items'])):
               
                descrp = result['items'][i]['description']
                summary = result['items'][i]['summary']
                descrp = descrp.strip()
                summary = summary.strip()
                guess_descrip = f'Polygon.IO: {polygon} | Nasdaq: {nasdaq} | MarketBeat: {mbeat}'
                guess_descrip =guess_descrip.strip()
                guess_summary = f'{ticker} has a split today'
                guess_summary =guess_summary.strip()

                if(descrp == guess_descrip):
                    
                    fail2 = 1  
            if(fail2 != 1):
                service.events().insert(calendarId=calendar_id, body=event).execute()

    np.savetxt("./Outputs/All_Dividends.csv", total_div,  fmt='%s',delimiter=",")
    np.savetxt("./Outputs/All_Earnings.csv", total_earn,  fmt='%s',delimiter=",")
    np.savetxt("./Outputs/All_Splits.csv", total_split,  fmt='%s',delimiter=",")

if __name__ == "__main__":
    main()