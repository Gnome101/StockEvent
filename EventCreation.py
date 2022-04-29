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
#end_time  = date + timedelta(hours = 12)
  event = {
    'summary': f'{ticker} has an ex-dividend date today' + Error,  
    'description': f'Polygon.IO: {polygon}\nNasdaq: {nasdaq}\nSeeking Alpha: {alpha}  ',
    'start': {
      'dateTime': date.strftime("%Y-%m-%dT6:0:0"),
      'timeZone': 'America/Los_Angeles',
    },
    'end': {
      'dateTime': date.strftime("%Y-%m-%dT16:0:0"),
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
def returnEarningTime(alert):
  if(alert == 1):
    time  = "AMC"
  elif(alert == 0):
    time = "BMO"
  elif(alert == -1):
    time = "UNK"
  elif(alert == -2):
    time = "UNK"
  return time
def createEarnEvent(ticker,service,nasdaq,yahoo,finviz, fin_alert ,yah_alert ): 
  #fin alert can be 0 or 1
  #yah alert can be 0, 1, or 2 
  if(fin_alert == yah_alert):
    if(fin_alert == 1):
      time = "AMC"
    elif(fin_alert ==0):
      time = "BMO"
    elif(fin_alert == -1):
      time = "UNK"
  elif(fin_alert != yah_alert):
    if(fin_alert == 1 and yah_alert == 0):
      time = "F-AMC | Y-BMO"
    elif(fin_alert == 0 and yah_alert == 1):
      time = "F-BMO | Y-AMC"
    elif(fin_alert == -1):
      time = returnEarningTime(yah_alert)
    elif(yah_alert == -1):
      time = returnEarningTime(fin_alert)
  alert = f"| {time}"

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
    
  #end_time  = date + timedelta(hours = 12)
  event = {
  'summary': f'{ticker} has earnings today' + Error + alert ,  
  'description': f'Nasdaq: {nasdaq}\nYahoo: {yahoo}\nFinviz: {finviz}',
  'start': {
    'dateTime': date.strftime("%Y-%m-%dT6:0:0"),
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': date.strftime("%Y-%m-%dT16:0:0"),
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
  #end_time  = date + timedelta(hours = 12)
  event = {
  'summary': f'{ticker} has a split today' + Error ,  
  'description': f'Polygon.IO: {polygon}\nNasdaq: {nasdaq}\nMarketBeat: {mbeat}',
  'start': {
    'dateTime': date.strftime("%Y-%m-%dT6:0:0"),
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': date.strftime("%Y-%m-%dT16:0:0"),
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