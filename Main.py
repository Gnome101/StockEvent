import time
import pandas as pd
import os
import Dividend as dv
import Earnings as er
from datetime import datetime, timedelta
import Splits as sp   
import GoogleCalendar as gc
import EventCreation as ec
import numpy as np
import random
from apiclient.discovery import build

def getLength(service, calendar_id):
    time.sleep(.5)
    result = service.events().list(calendarId =calendar_id, maxResults=9999  ).execute()
    return len(result['items'])
def findTime(a,b,c):
    fin_alert = a
    yah_alert = b
    nas_alert = c
    time = "Nothing"
    if(fin_alert == yah_alert and fin_alert == nas_alert):
        if(fin_alert == 1):
            time = "AMC"
        elif(fin_alert == 0):
            time = "BMO"
        elif(fin_alert == 2):
            time = "EST"
        elif(fin_alert == -1):
            time = "UNK"
    else:    
        if(nas_alert == -1 ):
            if(fin_alert == -1):              
                time = returnEarningTime(yah_alert)
            elif(nas_alert == 2):       
                time = returnEarningTime(nas_alert)
            else:        
                time = returnEarningTime(fin_alert)
        else:
            if(nas_alert != 2):
                time = returnEarningTime(nas_alert)
            else:
                if(fin_alert !=-1):
                    time = returnEarningTime(fin_alert)
                else:
                    time = returnEarningTime(nas_alert)
    return time
def isolateDates(guess_descrip):  
  loc1 = guess_descrip.find(":")
  loc2 = guess_descrip.find("00:")
  if(loc2 > loc1+16):
    date1 = guess_descrip[loc1+1:loc1+2].strip()
    guess_descrip2 = guess_descrip[loc1+2:]
  else:
    date1 = guess_descrip[loc1+1:loc2+8].strip()
    guess_descrip2 = guess_descrip[loc2+9:]
  #print("1: ",date1)

  loc1 = guess_descrip2.find(":")
  loc2 = guess_descrip2.find("00:")
  if(loc2 > loc1+16):
    date2 = guess_descrip2[loc1+1:loc1+2]
    guess_descrip2 = guess_descrip2[loc1+2:]
  else:
    date2 = guess_descrip2[loc1+1:loc2+8].strip()
    guess_descrip2 = guess_descrip2[loc2+9:]
  #print("2: ",date2)

  loc1 = guess_descrip2.find(":")
  loc2 = guess_descrip2.find("00:")
  if(loc2 > loc1+16):
    date3 = guess_descrip2[loc1+1:loc1+2]
  else:
    date3 = guess_descrip2[loc1+1:loc2+8].strip()
  #print("3: ",date3)
  return date1,date2,date3
def refresh(service, calendar_id):
    Info = pd.read_csv('./Inputs/Info.csv')
    longest_del = int(Info['Data'][9])
    delUNK = int(Info['Data'][10])   
    
    
    result = service.events().list(calendarId =calendar_id, maxResults=9999 ).execute()
    #print(result['items'])
    length = len(result['items'])
    print("Total amount of Events On Calendar:",length)
        
    for i in range(length):
        date = result['items'][i]['end']['dateTime'].strip()
        title = result['items'][i]['summary'].strip()
        loc = date.find("T")
        date = date[:loc]   
        date = datetime.strptime(date,'%Y-%m-%d')              
        if(date.date() < datetime.now().date() or date.date() > datetime.now().date() + timedelta(days = longest_del)  ):
            eventID = result['items'][i]['id']
            service.events().delete(calendarId=calendar_id, eventId=eventID).execute()        
        #elif ((title.find("UNK") >= 0 or title.find("EST") >= 0) and delUNK == 1):            
            #eventID = result['items'][i]['id']
            #service.events().delete(calendarId=calendar_id, eventId=eventID).execute()
        time.sleep(0.15)
    
def main():
    calendar_id,creds = gc.main()
    service = build("calendar", "v3",credentials= creds)
    refresh(service,calendar_id)    
    tickers_list = pd.read_csv('./Inputs/TickerList.csv')
    Info = pd.read_csv('./Inputs/Info.csv')
    sleep = int(Info['Data'][1])
    delUNK = int(Info['Data'][10])
    tickers_len = len(tickers_list) 

    Info = pd.read_csv('./Inputs/Info.csv')
    Calendar_Title = Info['Data'][0].strip()
    print(Calendar_Title)    

    #These contain the dates in a datetime object format. Size of each is same as amount of tickers
    poly_div = []
    poly_split = []
    nasdaq_div = []
    nasdaq_earn = []
    nasdaq_split = []
    yahoo_earn = []
    alpha_div = []
    finviz_earn = []
    marketbeat_split = []
    #These detail the designaitons of AMC, BMO, EST, and UNK
    finviz_after = []
    yahoo_after = []
    nasdaq_after = []
    #These ensure that the final count is only made when all are finished
    polycount = 0
    yahoocount = 0
    scrapecount = 0
    nascount = 0
    count = 0
    startTime = time.time()
    nasdaq_time_out = 0

    p1, p2, n1,n2,n3,y1,s = -65,-65,-65,-65,-65,-65,-65,
    pstop,nstop,ystop,sstop,mbstop,fstop = 0,0,0,0,0,0
    while(count < 9):
        prev_poly = polycount
        for i in range(5):
            if(polycount == tickers_len):
                polycount = 0
            ticker = tickers_list['Ticker'][polycount]

            #print(len(poly_split) != tickers_len,time.time()-p2 > 60, len(poly_div) == tickers_len)
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
        if(prev_poly != polycount):
            p1 = time.time()
            p2 = time.time()
        for i in range(1):
            if(nascount == tickers_len):
                nascount = 0
            ticker = tickers_list['Ticker'][nascount]
            if(len(nasdaq_div) != tickers_len and time.time()-n1 >= 30 + (random.random() * 5)):
                date = dv.nasdaq_div(ticker)
                nasdaq_div.append(date)
                nascount += 1
                n1=time.time()
            elif(len(nasdaq_earn) != tickers_len and time.time()-n2 >= 30 + (random.random() * 5) and len(nasdaq_div) == tickers_len):
                date, AMC = er.nasdaq_earn(ticker)
                nasdaq_earn.append(date)
                nasdaq_after.append(AMC)
                nascount += 1
                n2=time.time()                                                
            elif(len(nasdaq_split) != tickers_len and time.time()-n3 >= 30 + (random.random() * 4) and len(nasdaq_earn) == tickers_len  ):
                split_dates = sp.nasdaq_split(tickers_list)  
                print("nasdaq", split_dates)              
                nasdaq_split = split_dates
                nascount += 1
                n3=time.time()
                if(len(nasdaq_split) != tickers_len ):
                    nasdaq_time_out += 1
                if(nasdaq_time_out > 2):
                    print("Nasdaq timed out for splits, making empty ones")
                    for i in range(len(tickers_list)):
                        nasdaq_split.append("")
            elif(len(nasdaq_earn) == tickers_len and nstop == 0 and len(nasdaq_split) == tickers_len ):
                count += 3
                nstop = 1
        for i in range(5):
            if(yahoocount == tickers_len):
                yahoocount = 0
            ticker = tickers_list['Ticker'][yahoocount]
            if(len(yahoo_earn) != tickers_len and time.time()-y1 >= 30):
                date, AMC = er.yahoo_earn(ticker)
                yahoo_after.append(AMC)
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
            if(len(finviz_earn) != tickers_len and time.time()-s >= 30+ (random.random() * 3)):
                date, AMC =er.finviz_earn(ticker)
                finviz_after.append(AMC)
                finviz_earn.append(date)
            elif(len(finviz_earn) == tickers_len and fstop == 0 ):
                count += 1
                fstop = 1
            if(len(alpha_div) != tickers_len and time.time()-s >= 35+ (random.random() * 3)):
                date = dv.alpha_div(ticker)
                alpha_div.append(date)
                scrapecount += 1
                s = time.time()
            elif(len(alpha_div) == tickers_len and sstop == 0  ):
                count += 1
                sstop = 1
            if(len(marketbeat_split) != tickers_len and time.time()-s >= 35 + (random.random() * 2)):
                split_dates = sp.marketbeat_split(tickers_list)
                print("Marketbeat", split_dates)
                marketbeat_split = split_dates 
                print("Lengths:",len(marketbeat_split),tickers_len)               
            elif(len(marketbeat_split) == tickers_len and mbstop == 0  ) :                
                count+=1
                mbstop = 1
        pb1 = startTime
        pb2 = startTime
        nb2 = startTime
        nb3 = startTime
        if(p1 < 0):
            p1 = startTime + 0.1
        if(p2 > 0):
            pb2 = p2
        if(n2 > 0):
            nb2 = n2
        if(n3 > 0):
            nb3 = n3
                
        print("Waiting | Time since start for Polygon: ","Dividends:",round((p1- startTime),2),"Splits",round((pb2-startTime),2))
        print("Waiting | Time since start for  NasDaq","Dividends:", round((n1-startTime),2),"Earnings:", round((nb2-startTime),2),
        "Splits:",round((nb3- startTime),2))
        print("Waiting | Time since start for yahoo: ","Earnings:", round((y1-startTime),2))
        print("Waiting | Time since start for seeking alpha, finviz, and marketbeat: ",round((s-startTime),2))
        print("Number of finished ones:", count ,"Total Number of Tickers:",tickers_len ) 
        if(count != 9 ):
            sleep_add = round((random.random() * randsleep),2)
            print(f"Waiting for {round(sleep + sleep_add,2)} seconds now")
            time.sleep(sleep + sleep_add )
            "Finished"
                  
        
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
    #Check for mimicked events and check for updates events.  
    for i in range(len(total_div)):
        fail = 0
        fail2 = 0
        event, fail = ec.createDivEvent(total_div[i][0],service,total_div[i][1],total_div[i][2],total_div[i][3])
        #print(total_div[i][0])      
        if(fail != 1):
            ticker = total_div[i][0]
            polygon = total_div[i][1]
            nasdaq = total_div[i][2]
            alpha = total_div[i][3]
            result = service.events().list(calendarId =calendar_id, maxResults=9999  ).execute()
            #print(ticker, "Making dividend [2]")
            for i  in range(len(result['items'])):
               
                descrp = result['items'][i]['description']
                summary = result['items'][i]['summary']
                #remind = result['items'][i]['reminders']

                descrp = descrp.strip()
                summary = summary.strip()
                #remind = remind.strip()

                guess_descrip = f'Polygon.IO: {polygon}\nNasdaq: {nasdaq}\nSeeking Alpha: {alpha}'
                guess_descrip =guess_descrip.strip()
                guess_summary = f'{ticker} has an ex-dividend date today'
                guess_summary = guess_summary.strip()

                date1 , date2, date3 = isolateDates(guess_descrip)
                if(nasdaq.strip() == date1 or yahoo.strip() == date1 or finviz.strip() == date1):
                     nothing= 0
                else:
                    fail2 = 0
                if(nasdaq.strip() != date2 or yahoo.strip() != date2 or finviz.strip() != date2):
                    nothing= 0
                else:
                    fail2 = 0
                if(nasdaq.strip() != date3 or yahoo.strip() != date3 or finviz.strip() != date3):
                     nothing= 0
                else:
                    fail2 = 0  
            if(fail2 != 1):
                #print(ticker, "Making dividend [3]",fail,fail2)
                cal_length = getLength(service,calendar_id)
                #print(cal_length)
                PROCEED = 0
                while(PROCEED == 0):
                    service.events().insert(calendarId=calendar_id, body=event).execute()
                    if(getLength(service,calendar_id) > cal_length):
                        PROCEED = 1
                    else:
                        COUNT = COUNT +1
                        print("Failed to create dividend event, trying again")
                        time.sleep(COUNT)
                        if(COUNT == 3):
                            print("Skipping event creation")
                            PROCEED = 1

    for i in range(len(total_earn)):
        fail = 0
        fail2 = 0
        nasdaq_after_alert = nasdaq_after[i]
        finviz_after_alert = finviz_after[i]
        yahoo_after_alert = yahoo_after[i]        
        event, fail = ec.createEarnEvent(total_earn[i][0],service,total_earn[i][1],total_earn[i][2],total_earn[i][3],nasdaq_after_alert,finviz_after_alert,yahoo_after_alert)
        if(fail != 1):
            ticker = total_div[i][0]
            nasdaq = total_earn[i][1]
            yahoo = total_earn[i][2]
            finviz = total_earn[i][3]

            finviz_after_alert = finviz_after[i]
            yahoo_after_alert = yahoo_after[i]
            nasdaq_after_alert = nasdaq_after[i]
            a = finviz_after_alert
            b = yahoo_after_alert
            c = nasdaq_after_alert
            result = service.events().list(calendarId =calendar_id, maxResults=9999  ).execute()            
            for i  in range(len(result['items'])):
               
                descrp = result['items'][i]['description']
                summary = result['items'][i]['summary']
                descrp = descrp.strip()
                summary = summary.strip()
                guess_descrip = f'Nasdaq: {nasdaq}\nYahoo: {yahoo}\nFinviz: {finviz}'
                guess_descrip =guess_descrip.strip()
                guess_summary = f'{ticker} has earnings today'
                guess_summary =guess_summary.strip()
                print(ticker,"Equal Events",descrp == guess_descrip and summary.find(guess_summary) >= 0)    
                loc = guess_summary.find("today")
                if(summary.find(guess_summary[:loc+5]) >= 0 ):
                    if summary.find("BMO") >= 0 or summary.find("AMC") >= 0 :
                        date1 ,date2,date3 = isolateDates(guess_descrip)
                        if(findTime(a,b,c)=="AMC" or findTime(a,b,c) == "BMO"):
                            if(nasdaq.strip() == date1 or yahoo.strip() == date1 or finviz.strip() == date1):
                                nothing = 0
                            else:
                                fail2=0
                            if(nasdaq.strip() != date2 or yahoo.strip() != date2 or finviz.strip() != date2):
                                nothing = 0
                            else:
                                fail2=0
                            if(nasdaq.strip() != date3 or yahoo.strip() != date3 or finviz. strip() != date3):
                                nothing = 0
                            else:
                                fail2=0   
                        else:
                            fail2 = 1
                    else:
                        if (findTime(finviz_after_alert,yahoo_after_alert,nasdaq_after_alert) == "AMC" or findTime(finviz_after_alert,yahoo_after_alert,nasdaq_after_alert) == "BMO"): 
                            fail2 = 0              
                        else:
                            if(delUNK == 1):
                                #eventID = result['items'][i]['id']
                                #service.events().delete(calendarId=calendar_id, eventId=eventID).execute()
                                print("delete")                             
                            else:
                                fail2=1
            if(fail2 != 1):
                cal_length = getLength(service,calendar_id)
                PROCEED = 0
                COUNT = 0
                while(PROCEED == 0):
                    service.events().insert(calendarId=calendar_id, body=event).execute()
                    if(getLength(service,calendar_id) > cal_length):
                        PROCEED = 1
                    else:
                        COUNT = COUNT +1
                        print("Failed to create earnings event, trying again")
                        time.sleep(COUNT)
                        if(COUNT == 3):
                            print("Skipping event creation")
                            PROCEED = 1
    for i in range(len(total_split)):
        fail = 0
        fail2 = 0
        event, fail = ec.createSplitEvent(total_split[i][0],service,total_split[i][1],total_split[i][2],total_split[i][3])
        if(fail != 1):
            ticker = total_div[i][0]
            polygon = total_split[i][1]
            nasdaq = total_split[i][2]
            mbeat = total_split[i][3]
            result = service.events().list(calendarId =calendar_id, maxResults=9999  ).execute()
            for i  in range(len(result['items'])):
               
                descrp = result['items'][i]['description']
                summary = result['items'][i]['summary']
                descrp = descrp.strip()
                summary = summary.strip()
                guess_descrip = f'Polygon.IO: {polygon}\nNasdaq: {nasdaq}\nMarketBeat: {mbeat}'
                guess_descrip =guess_descrip.strip()
                guess_summary = f'{ticker} has a split today'
                guess_summary =guess_summary.strip()

                date1 , date2, date3 = isolateDates(guess_descrip)
                if(nasdaq.strip() == date1 or yahoo.strip() == date1 or finviz.strip() == date1):
                     nothing= 0
                else:
                    fail2 = 0
                if(nasdaq.strip() != date2 or yahoo.strip() != date2 or finviz.strip() != date2):
                    nothing= 0
                else:
                    fail2 = 0
                if(nasdaq.strip() != date3 or yahoo.strip() != date3 or finviz.strip() != date3):
                     nothing= 0
                else:
                    fail2 = 0   
            if(fail2 != 1):
                cal_length = getLength(service,calendar_id)
                PROCEED = 0
                while(PROCEED == 0):
                    service.events().insert(calendarId=calendar_id, body=event).execute()
                    if(getLength(service,calendar_id) > cal_length):
                        PROCEED = 1
                    else:
                        COUNT = COUNT +1
                        print("Failed to create split event, trying again")
                        time.sleep(COUNT)
                        if(COUNT == 3):
                            print("Skipping event creation")
                            PROCEED = 1

    #np.savetxt("./Outputs/All_Dividends.csv", total_div,  fmt='%s',delimiter=",")
    #np.savetxt("./Outputs/All_Earnings.csv", total_earn,  fmt='%s',delimiter=",")
    #np.savetxt("./Outputs/All_Splits.csv", total_split,  fmt='%s',delimiter=",")

if __name__ == "__main__":
    
    tickers_list = pd.read_csv('./Inputs/TickerList.csv')
    Info = pd.read_csv('./Inputs/Info.csv')
    randsleep = int(Info['Data'][2])
    days_run = Info['Data'][7]
    days_array = []
    print(days_run)
    for i in range(len(days_run)):
        days_array.append(int(days_run[i]))
    print(days_array)
    today = datetime.now()    
    day = today.weekday()
    print(day)
    count = 0
    for i in range(len(days_array)):
        if(day == days_array[i]):            
            count += 1
            
    if(count > 0):
       main()  
    else:
        print("Not scheduled day")
            
        
  
    