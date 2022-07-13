import requests
import yahoo_fin.stock_info as si
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
#Used to get environment variables
import os
tickers_list = pd.read_csv('./Inputs/TickerList.csv')
Info = pd.read_csv('./Inputs/Info.csv')
longest = int(Info['Data'][8])
def polyio_split(ticker):
    fail = 0
    apikeyPoly = os.environ["POLYGON_KEY"] 
    apikeyPoly = apikeyPoly.strip()
    api_url_dividends = f'https://api.polygon.io/v3/reference/splits?ticker={ticker}&apiKey={apikeyPoly}'
    print("From Polygon.IO Pulling","for", ticker, "Splits")
    try:
        data_dividend = requests.get(api_url_dividends).json()
    
        print(data_dividend)
        if(data_dividend['results'] == []) or fail == 1:
            date = ""
        else:
            date = data_dividend['results'][0]['execution_date']
            date = datetime.strptime(date, '%Y-%m-%d')
            if(date.date() < datetime.now().date() or date.date() > datetime.now().date() + timedelta(days=longest)):
                date = "" 
    except:
        date = ""
        fail = 1
    return date 
def nasdaq_split(ticker_list):
   
    fail = 0
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
   
    try:
        if "IPB_HTTP" in os.environ:    
            proxyDict = {
                "http"  : os.environ.get('IPB_HTTP', ''),
                "https" : os.environ.get('IPB_HTTPS', '')
                }    
            response = requests.get('https://api.nasdaq.com/api/calendar/splits', headers=headers, proxies=proxyDict)
        else:
            response = requests.get('https://api.nasdaq.com/api/calendar/splits', headers=headers)
        print("From NasDaq Pulling",response, "for", "Splits")
        response_json = response.json()
        split_data = response_json['data']['rows']
        split_date = ""        
    except:
        split_date = ""
        fail = 1
        print("Error in pulling Nasdaq splits")
    split_dates = []
    found_tickers = []
    count = 0
    if( fail != 1):
        for i in range(len(split_data)):
            found_ticker = split_data[i]['symbol'].strip()
            found_tickers.append(found_ticker)

    
    for i in range(len(ticker_list)): 
        count = 0     
        ticker = ticker_list['Ticker'][i].strip()
        for i in range(len(found_tickers)):
            found_ticker = found_tickers[i].strip()
                    
            if(found_ticker ==  ticker):            
                split_date = split_data[i]['executionDate']            
                split_date = datetime.strptime(split_date, '%m/%d/%Y')               
                if(split_date.date() < datetime.now().date() or split_date.date() > datetime.now().date() + timedelta(days=longest)):             
                    split_date = "" 
                    split_dates.append(split_date)
                else:              
                    split_dates.append(split_date)
            else:
                split_date = ""
                count += 1 
            if(count == len(found_tickers)):
                    split_dates.append("") 

    return split_dates
def marketbeat_split(ticker_list):
    def tableDataText(table):  
        #Code adjusted from https://stackoverflow.com/questions/2935658/beautifulsoup-get-the-contents-of-a-specific-table  
        """Parses a html segment started with tag <table> followed 
        by multiple <tr> (table rows) and inner <td> (table data) tags. 
        It returns a list of rows with inner columns. 
        Accepts only one <th> (table header/data) in the first row.
        """
        def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
            return [td.get_text(strip=True) for td in tr.find_all(coltag)]  
        rows = []
        trs = table.find_all('tr')
        headerow = rowgetDataText(trs[0], 'th')
        if headerow: # if there is a header row include first
            rows.append(headerow)
            trs = trs[1:]
        for tr in trs: # for every table row
            rows.append(rowgetDataText(tr, 'td') ) # data row       
        return rows
    try:
        url = f'https://www.marketbeat.com/stock-splits/'
        
        response_html=requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        print("From MarketBeat Pulling","for all", "Splits")
        soup = BeautifulSoup(response_html.content, 'html.parser')

        
        htmltable = soup.find('table', { 'class' : 'scroll-table sort-table' })
        list_table = tableDataText(htmltable)
        split_date = "" 
        found_tickers = []
        
        for i in range(len(list_table)):
            company = list_table[i][0]
            ticker_index = i
            for i in range(len(company)):
                if(company[i].islower()):               
                    
                    found_ticker = company[:i-1] 
                    found_tickers.append(found_ticker)               
                    break
    except:
        print("Exception")         
        split_dates = []
    
    for i in range(len(ticker_list)):  
            count = 0    
            ticker = ticker_list['Ticker'][i].strip()
            for i in range(len(found_tickers)):
                found_ticker = found_tickers[i].strip()
                     
                if(found_ticker ==  ticker): 
                    diff = len(list_table) - len(found_tickers)
                    split_date = list_table[i+diff][3]                 
                                        
                    split_date = datetime.strptime(split_date, '%m/%d/%Y')                
                    if(split_date.date() < datetime.now().date() or split_date.date() > datetime.now().date() + timedelta(days=longest)):
                        split_date = ""
                        split_dates.append(split_date)   
                    else:
                        split_dates.append(split_date)                 
                else:
                    split_date = ""
                    count += 1 
                if(count == len(found_tickers)):
                    split_dates.append("")
    
    return split_dates
    
 



