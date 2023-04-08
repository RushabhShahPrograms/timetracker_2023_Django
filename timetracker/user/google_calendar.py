from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from timetracker.settings import GOOGLE_API_KEY

SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None
if GOOGLE_API_KEY:
    creds = service_account.Credentials.from_service_account_info(
        GOOGLE_API_KEY, scopes=SCOPES)

service = build('calendar', 'v3', credentials=creds)