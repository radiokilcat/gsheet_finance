from __future__ import print_function
import pickle
import os.path
import configparser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint

from parse_tinkoff_data import get_expenses_from_csv

config = configparser.ConfigParser()
config.read("config.ini")

SCOPES = [config['DEFAULT']['SCOPES']]
SAMPLE_SPREADSHEET_ID = config['DEFAULT']['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = config['DEFAULT']['SAMPLE_RANGE_NAME']
csv_path = config['DEFAULT']['csv_path']


def parse_csv(csv):
    with open(csv, "r", encoding='cp1251') as f_obj:
        return get_expenses_from_csv(f_obj)

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    tinkoff_int_data = list(parse_csv(csv_path).values())

    new_values = {
        'values': [tinkoff_int_data],
        'majorDimension': 'COLUMNS'
    }

    result = sheet.values().update(
       spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED", body=new_values).execute()


if __name__ == '__main__':
    main()