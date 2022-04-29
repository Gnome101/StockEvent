#Used to make the requests
import requests
#Used for the manipulation of the data
import pandas as pd
#Used to make the program wait in between calls
import time
#Used to get current date and to create a date object that is easy to compare
from datetime import datetime , timedelta
#Used to get earnings data
from bs4 import BeautifulSoup
import os
import yahoo_fin.stock_info as si

def nasdaq_earn(ticker):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nasdaq.com/',
    'Origin': 'https://www.nasdaq.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Cache-Control': 'max-age=0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }
    proxyDict = {
              "http"  : os.environ.get('IPB_HTTP', ''),
              "https" : os.environ.get('IPB_HTTPS', '')
            }
    try:
        response = requests.get(f'https://api.nasdaq.com/api/analyst/{ticker}/earnings-date', headers=headers, proxies=proxyDict)
        print("From NasDaq Pulling",response, "for", ticker, "Earnings")
        response_json = response.json() 
        date = response_json['data']['announcement']
    
        start = date.find(':') +1
        end = len(date)
        earn_date = date[start:end]
    
        earn_date = earn_date.strip()
        earn_date = datetime.strptime(earn_date, '%b %d, %Y')
    except:
        earn_date = datetime(9999,12,12,0,0)
    if(earn_date.date() < datetime.now().date()):
          earn_date = ""
    
    return earn_date

def finviz_earn(ticker):


    add_day = 0    
    
    url = f'https://finviz.com/quote.ashx?t={ticker}'
    response = ''
    try:
        response_html=requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        print("From Finviz Pulling", "for", ticker, "Earnings")
        soup = BeautifulSoup(response_html.content, 'html.parser')
        
        html = list(soup.children)[2]
        
        
        body = list(html.children)[3]
        
        tbl = list(body.children)[12]
        
        indv = list(tbl.children)[0]    
        
        cell = list(indv.children)[5]
        
        group = list(cell.children)[21]
    
        single = list(group.children)[8]
        
        b = list(single.children)[0]
        earn_date = b.get_text()
        
        if(earn_date.find("AMC") != -1):
            add_day = 1
        earn_date = earn_date[:6]
    
        year = str(datetime.now().year)
        earn_date = year +" "+ earn_date
        earn_date = datetime.strptime(earn_date, '%Y %b %d')
        earn_date = earn_date + timedelta(days = add_day)
        
        if(earn_date.date() < datetime.now().date()):
            earn_date = ""
    except:
        earn_date = "" 
    return earn_date
def yahoo_earn(ticker):
    try:
        earn_date = si.get_next_earnings_date(ticker)
        if(earn_date.date() < datetime.now().date()):
            earn_date = "" 
    except Exception as ex:
        earn_date = ""
    print("From Yahoo Pulling",earn_date ,"for", ticker, "Earnings")
    
    return earn_date
     