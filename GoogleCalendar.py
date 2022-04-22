from apiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client
from google.auth.transport.requests import Request
import pickle
import os


scopes = ['https://www.googleapis.com/auth/calendar']

def main(title):
    creds = None
    CONTENTS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    creds = client.Credentials.new_from_json(CONTENTS)
            
           
    service = build("calendar", "v3",credentials= creds)
    result = service.calendarList().list().execute()    
    calendars = result['items']
    
    for i in range(len(calendars)):
        if(calendars[i]['summary'].strip() == title):
            index = i
    sum = calendars[index]['summary']   
    id =  calendars[index]['id']      
    return id,creds    

