from datetime import datetime , timedelta
import pandas as pd
tickers_list = pd.read_csv('./Inputs/TickerList.csv')
Info = pd.read_csv('./Inputs/Info.csv')
remind_1_length = int(Info['Data'][3])
remind_1_type = (Info['Data'][4]).strip()
remind_2_length = int(Info['Data'][5])
remind_2_type = (Info['Data'][6]).strip()
def createDivEvent(ticker,service,polygon,nasdaq,alpha ):
  
  fail = 0
  date = nasdaq
  Error =""
  if((polygon == nasdaq) and(nasdaq == alpha)):
    Error = ""
  else:
    Error = " | Discrepancy!"
    
  if(nasdaq != ""):   
    date =  nasdaq
  elif(polygon != ""):
    date = polygon
  elif(alpha != ""):
    date = alpha
  else:
    fail = 1
    date = datetime.now()        

  end_time  = date + timedelta(hours = 12)
  event = {
    'summary': f'{ticker} has an ex-dividend date today' + Error,  
    'description': f'Polygon.IO: {polygon}\nNasdaq: {nasdaq}\nSeeking Alpha: {alpha}  ',
    'start': {
      'dateTime': date.strftime("%Y-%m-%dT%H:%M:%S"),
      'timeZone': 'America/Los_Angeles',
    },
    'end': {
      'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
      'timeZone': 'America/Los_Angeles',
      },  
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': remind_1_type, 'minutes':remind_1_length},
        {'method': remind_2_type, 'minutes': remind_2_length},
        
      ],
      },
      
  }
  return event, fail
def createEarnEvent(ticker,service,nasdaq,yahoo,finviz ):  
  fail = 0
  Error =""
  if((nasdaq == yahoo) and (yahoo == finviz)):
    Error = ""
  else:
    Error = " | Discrepancy!"
  if(nasdaq != ""):
    date = nasdaq 
  elif(yahoo != ""):
    date = yahoo
  elif(finviz != ""):
    date = finviz
  else:
    fail = 1
    date = datetime.now()
    
  end_time  = date + timedelta(hours = 12)
  event = {
  'summary': f'{ticker} has earnings today' + Error,  
  'description': f'Nasdaq: {nasdaq}\nYahoo: {yahoo}\nFinviz: {finviz}',
  'start': {
    'dateTime': date.strftime("%Y-%m-%dT%H:%M:%S"),
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    'timeZone': 'America/Los_Angeles',
    },  
  'reminders': {
    'useDefault': False,
    'overrides': [
       {'method': remind_1_type, 'minutes':remind_1_length},
       {'method': remind_2_type, 'minutes': remind_2_length},
    ],
    },
    }
  return event, fail
def createSplitEvent(ticker,service,polygon,nasdaq,mbeat):
  fail = 0
  Error =""
  if( (polygon == nasdaq) and (nasdaq == mbeat)):
    Error = ""
  else:
    Error = " | Discrepancy!"
  if(nasdaq != ""):
    date = nasdaq
  elif(polygon != ""):
    date = polygon
  elif(mbeat != ""):
    date = mbeat
  else:
    fail = 1
    date = datetime.now()
  end_time  = date + timedelta(hours = 12)
  event = {
  'summary': f'{ticker} has a split today' + Error ,  
  'description': f'Polygon.IO: {polygon}\nNasdaq: {nasdaq}\nMarketBeat: {mbeat}',
  'start': {
    'dateTime': date.strftime("%Y-%m-%dT%H:%M:%S"),
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    'timeZone': 'America/Los_Angeles',
    },  
  'reminders': {
    'useDefault': False,
    'overrides': [
       {'method': remind_1_type, 'minutes':remind_1_length},
       {'method': remind_2_type, 'minutes': remind_2_length},
    ],
    },
    }
  return event, fail  