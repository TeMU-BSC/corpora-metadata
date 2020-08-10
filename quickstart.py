'''
To run this script you need the 'credentials.json' file. To get it, follow the
steps in the documentation of the Google Sheets API v4:
https://developers.google.com/sheets/api/quickstart/python

The TEMU's Corpora Metadata has been registered through the following Google form:
https://docs.google.com/forms/d/1D5BQc3hMKuOL6jrsNdICXeKga5iCRCjpMHrwR83LYDM

and its answers are being stored in this Google spreadsheet:
https://docs.google.com/spreadsheets/d/1M2BrRHwWmG4zclofFviPQrg9V67kNmx13GuK3od1jtw

Languages codes have been found in the library:
https://pypi.org/project/iso-language-codes/
'''

import pickle
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from iso_language_codes import language, language_name, language_dictionary

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a spreadsheet.
SPREADSHEET_ID = '1M2BrRHwWmG4zclofFviPQrg9V67kNmx13GuK3od1jtw'
RANGE_NAME = 'Answers!A1:AI'

# langs_codes = dict(catalan='ca', english='en', spanish='es', basque='eu', finnish='fi', georgian='ka', kazah='kk',
#                    latvian='lv', ukrainan='uk', norwegian='no')
# open('languages.json', 'w').write(json.dumps(language_dictionary(), ensure_ascii=False, sort_keys=True, indent=4))


def to_snake_case(input: str) -> str:
    return input.replace(' ', '_').lower()


def language_code(language_name: str) -> str:
    '''Return the language code for a given language name.'''
    for lang in language_dictionary().items():
        code = lang[0]
        info = lang[1]
        if info.get('Name') == language_name:
            return code


def set_state():
    pass


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    question_titles = values[0]
    question_titles[0] = 'timestamp'
    question_titles[2] = 'email_address'
    fieldnames = question_titles
    rows = values[1:]
    keys = [to_snake_case(field) for field in fieldnames]
    # print(keys)
    data = [dict(zip(keys, row)) for row in rows]

    open('responses.json', 'w').write(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    main()
