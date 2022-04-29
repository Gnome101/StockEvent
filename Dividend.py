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
#Used to get environment variables
import os



def nasdaq_div(ticker):
    #Decleration of headers and params for the webscraping
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

    params = { 'assetclass': 'stocks'}
    proxyDict = {
              "http"  : os.environ.get('IPB_HTTP', ''),
              "https" : os.environ.get('IPB_HTTPS', '')
            }
    try:
      response = requests.get(f'https://api.nasdaq.com/api/quote/{ticker}/dividends', headers=headers, params=params, proxies=proxyDict)
      print(resonse)
      print("From NasDaq Pulling","for", ticker.strip(), "Dividends")
      response_json = response.json() 
      dividend_data = response_json['data']
      if(dividend_data['exDividendDate'] == 'N/A'):
          date = ""
      else:
          date = dividend_data['dividends']['rows'][0]['exOrEffDate']
          date = datetime.strptime(date, '%m/%d/%Y')        
          if(date.date() < datetime.now().date()):
            date = ""    
    except:
      date = ""
    return date
def alpha_div(ticker):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'https://seekingalpha.com/symbol/{ticker}/dividends/history',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'machine_cookie=3656728088431; LAST_VISITED_PAGE=%7B%22pathname%22%3A%22https%3A%2F%2Fseekingalpha.com%2Fsymbol%2FIBM%2Fdividends%2Fhistory%22%2C%22pageKey%22%3A%2279311d25-9661-44f3-ac30-76f5f9a5f679%22%7D; sailthru_pageviews=2; _gcl_au=1.1.821589720.1649812678; prism_25946650=dd07cf33-f323-4d2b-b92a-24fae7b80c06; _ga=GA1.2.1862537942.1649812680; _gid=GA1.2.676006977.1649812680; _hjSessionUser_65666=eyJpZCI6IjEzY2Y4MTZhLTU0N2ItNTYzZC05ODcxLTk0ZGFjYjk4YzA1NSIsImNyZWF0ZWQiOjE2NDk4MTI2ODA1NTYsImV4aXN0aW5nIjp0cnVlfQ==; _hjFirstSeen=1; _hjIncludedInSessionSample=1; _hjSession_65666=eyJpZCI6IjA3NjU0OTZkLTgwOGQtNGRkYS05YTMwLThkODlhNjQxNzdlZiIsImNyZWF0ZWQiOjE2NDk4MTI2ODA1OTksImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _hjCachedUserAttributes=eyJhdHRyaWJ1dGVzIjp7ImxvZ2dlZF9pbiI6ZmFsc2UsIm1wX3N1YiI6dHJ1ZSwicHJlbWl1bV9zdWIiOmZhbHNlLCJwcm9fc3ViIjpmYWxzZX0sInVzZXJJZCI6bnVsbH0=; __pat=-14400000; __pvi=%7B%22id%22%3A%22v-2022-04-12-18-17-57-742-qlxjQ8MghHMqVj6w-814401fb950576e7d351f2177133a69a%22%2C%22domain%22%3A%22.seekingalpha.com%22%2C%22time%22%3A1649812797430%7D; xbc=%7Bkpex%7Db104msXhX6qza57T_73BqZ0AhCCJGkxruWH3DBAOp5fPpCPoqw8tolSsk6M0-mYSlGA2s-BVUjntT0KXhjYD5q-mW2ZkIF_ptKc-mCw_PuxcxTtV1WGXEmGGXzL2dYIWGJQ-32V3iCzIgi1XruiPtUpUdanyvPvIYjEyQzZvVozNeRJNKzjYGn4-LGHkeb7wwletFBbbodKVd1lf-c9SFg; _px2=eyJ1IjoiOWJhYTk5ZjAtYmFjNy0xMWVjLTk2ZDctYjdjOWQ3M2M1MzU4IiwidiI6IjhlNjE5MzBkLWJhYzctMTFlYy05ZDE1LTc2NDQ1OTYzNTQ2MyIsInQiOjE2NDk4MTMyODY1NDcsImgiOiI5YTI5ZjE5OTQ2MWZmZWU1YmYwYTk2Yjc3ODgyY2UwMTY5MzAwYmVlNTU3N2M5NzZiMzlmYTM2YThmNTljZDQ3In0=; _px=Iz0uUwDIkHx/GqCuNy3QUYV63uAXp5YWZl1ZLtUWidKZJJ03io5zC1UeTp/52Komb2Nag0neXp2CzM5q8UPjsQ==:1000:tbVzg9KBwK2516ju/TCPTL36wp7bkD7KM3nDEZ5C2wLehx5a63i8EZD+ZnRgV2EuEkdZp6vl6Jd0a7TniGpQASuJW0Y1Yf9oXANlG38aHXnz2lVJ/mJ/MBT+2jh9P5gqzwVGLDxRuVXAhUCq1whGkgGU9WLVocC+sNsyrGFqdj1hCLLl+zqBOuBLvdM5ww6cZMRschbI66/feVC++Bn5H1CenT+rrdsZKm2RZ72CNN3x0WdPvfhlrSQZxGr/qqHvPK/Nr+0sf2k6IM89qvB58A==; pxcts=8e619abf-bac7-11ec-9d15-764459635463; _pxvid=8e61930d-bac7-11ec-9d15-764459635463; _pxde=e14f2b418bf13c0b414e0772bbe8ec881e183c58153a885465118c52bda14456:eyJ0aW1lc3RhbXAiOjE2NDk4MTI3ODg4MjgsImZfa2IiOjB9; _clck=16xpzat|1|f0l|0; _clsk=f5q3xy|1649812715735|2|0|i.clarity.ms/collect; __tbc=%7Bkpex%7Dr2p6DNHyCvQiadcb9sEQgw0DJAUhj82xAmznTj_KnpTKJwdxQFE03gy0LPgSXAal60uBP_GA04FnMPscOkbWPikh-TQHeKjP2fBflc1axAc; sailthru_content=d8a3c05f5cc4531a9bbb7b0d6e52fd48; sailthru_visitor=59f548d8-3038-47d3-9bfb-dd47ccc434b8; _cc_id=d4b3a4129d4ac09c89f0c30f4724d122; panoramaId_expiry=1650417506859; panoramaId=066ff2abc0a801ef969ff7e4ce6c4945a70299ab538e3bdd15e92e3ab99c67af; session_id=149b0d96-b016-4c13-82ff-982251b76c6e; _uetsid=8dddb1f0bac711ecafeae9798877737d; _uetvid=8dddbfd0bac711ecba0b4d0d3bf8e195',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'If-None-Match': 'W/f66354d7f9108a97fa299430d1dc7f5e',
         # Requests doesn't support trailers
         # 'TE': 'trailers',
    }

    params = {
      'group_by': 'quarterly',
      'sort': '-date',
    }

    try:
      response = requests.get(f'https://seekingalpha.com/api/v3/symbols/{ticker}/dividend_history', headers=headers, params=params)
      print("From Seeking Alpha Pulling",response,"for", ticker, "Dividends")
      response_json = response.json()       
      dividend_data = response_json['data']
      if(dividend_data == []):
        date = ""
      else:
        date = dividend_data[0]['attributes']['ex_date']
        date = datetime.strptime(date, '%Y-%m-%d')        
        if(date.date() < datetime.now().date()):
          date = "" 
    except:
      date = ""

    return date
def polyio_div(ticker):
    try:
      now = datetime.now()
      apikeyPoly = os.environ["POLYGON_KEY"] 
      
      apikeyPoly = apikeyPoly.strip()
      api_url_dividends = f'https://api.polygon.io/v3/reference/dividends?ticker={ticker}&apiKey={apikeyPoly}'
      print("From Polygon.IO Pulling","for", ticker, "Dividends")
      data_dividend = requests.get(api_url_dividends).json()
      
      if(data_dividend['results'] == []):
          date = ""
      else:
          date = data_dividend['results'][0]['ex_dividend_date']
          date = datetime.strptime(date, '%Y-%m-%d')
          if(date.date() < datetime.now().date()):
            date = "" 
    except:
      date = ""      
    return date 
   
    
     