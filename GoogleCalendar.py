from apiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import json
import requests
import os




def main():
    
    SERVICE_ACCOUNT = os.environ["SERVICE_ACCOUNT"]
    
    service_json = json.loads(SERVICE_ACCOUNT,strict=False)
    scopes = ['https://www.googleapis.com/auth/calendar']
    creds = service_account.Credentials.from_service_account_info(service_json,scopes=scopes)
    service = build("calendar", "v3",credentials= creds)   
   
    calendar_ID = os.environ["CALENDAR_ID"]   
    return calendar_ID,creds    
