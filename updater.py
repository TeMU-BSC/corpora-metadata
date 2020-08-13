'''
Create or update the 'metadata.json' file for TEMU's corpora in Data Transfer 1 (dt01.bsc.es:/gpfs/projects/bsc88/corpora).

Author: alejandro.asensio@bsc.es

To run this script you need the 'credentials.json' file. To get it, follow the steps in the documentation of the Google Sheets API v4:
https://developers.google.com/sheets/api/quickstart/python

The TEMU's Corpora Metadata has been registered through the following Google form:
https://docs.google.com/forms/d/1D5BQc3hMKuOL6jrsNdICXeKga5iCRCjpMHrwR83LYDM

and its answers are being stored in this Google spreadsheet:
https://docs.google.com/spreadsheets/d/1M2BrRHwWmG4zclofFviPQrg9V67kNmx13GuK3od1jtw

Language official ISO codes and names have been found in the library:
https://pypi.org/project/iso-language-codes/
'''

import pickle
import os.path
import json
from dataclasses import dataclass
from itertools import zip_longest
from typing import List

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from iso_language_codes import language, language_name, language_dictionary

from constants import (LANGUAGES_FILENAME, METADATA_FILENAME,
                       CORPUS_KEYS, VERSION_KEYS, STATE_KEYS,
                       LIST_KEYS)

# Save language codes and names into a json file.
# with open(LANGUAGES_FILENAME, 'w') as f:
#     json.dump(language_dictionary(), f, ensure_ascii=False, indent=2)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a spreadsheet.
SPREADSHEET_ID = '1M2BrRHwWmG4zclofFviPQrg9V67kNmx13GuK3od1jtw'
RANGE_NAME = 'Answers!A1:AJ'


def to_snake_case(input: str) -> str:
    return input.replace(' ', '_').lower()


def language_code(language_name: str) -> str:
    '''Return the language code for a given language name.'''
    for code, info in language_dictionary().items():
        if info.get('Name') == language_name:
            return code


def set_corpus(row: dict) -> dict:
    '''Build a corpus object.'''
    corpus = {k: row.get(k) for k in CORPUS_KEYS}
    corpus['versions'] = [set_version(row)]
    return corpus


def set_version(row: dict) -> dict:
    '''Build a version object.'''
    version = {k: row.get(k) for k in VERSION_KEYS}
    version['states'] = [set_state(row)]
    return version


def set_state(row: dict) -> dict:
    '''Build a state object.'''
    state = {k: row.get(k) for k in STATE_KEYS}
    return state


def build_metadata(rows: List[dict]) -> List[dict]:
    '''Build the metadata structure for registered corpora.'''
    metadata = list()

    # Separate responses by type.
    new_corpora = list()
    new_versions = list()
    new_states = list()
    for row in rows:
        # Convert checkbox form fields into lists of strings and trim whitespaces from string values.
        row = {k: v.split(', ') if v and k in LIST_KEYS else v.strip() if isinstance(v, str) else v
               for k, v in row.items()}
        # Find each type of response.
        if row.get('i_want_to_register_a_new:') == 'Corpus':
            new_corpora.append(row)
        elif row.get('i_want_to_register_a_new:') == 'Version':
            new_versions.append(row)
        elif row.get('i_want_to_register_a_new:') == 'State':
            new_states.append(row)

    # New corpus registers are primary objects in metadata list.
    metadata = [set_corpus(row) for row in new_corpora]

    # New versions need to find their belonging corpus path.
    for row in new_versions:
        version = set_version(row)
        parent_corpus_path = version.get('version_path').split('/')[0]
        for corpus in metadata:
            if corpus.get('corpus_path') == parent_corpus_path:
                corpus['versions'].append(version)

    # New states need to find their belonging version path.
    for row in new_states:
        state = set_state(row)
        parent_corpus_path = state.get('state_path').split('/')[0]
        version_number = state.get('state_path').split('/')[1]
        parent_version_path = f'{parent_corpus_path}/{version_number}'
        for corpus in metadata:
            if corpus.get('corpus_path') == parent_corpus_path:
                for version in corpus.get('versions'):
                    if version.get('version_path') == parent_version_path:
                        version['states'].append(state)

    # Return the resulting nested corpus/versions/states structure.
    return metadata


def main():
    '''Shows basic usage of the Sheets API. Prints values from a sample spreadsheet.'''
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

    # Preprocess the raw data from the spreadsheet.
    questions = values[0]
    responses = values[1:]
    questions[0] = 'timestamp'  # last update through google form edit link
    questions[2] = 'email_address'  # person who has recorded the metadata
    headings = [to_snake_case(question) for question in questions]
    rows = [dict(zip_longest(headings, response)) for response in responses]

    # Save the form responses (spreadsheet rows) into a json file just for reference.
    with open('responses.json', 'w') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    # Save processed rows into the final metadata file.
    with open(METADATA_FILENAME, 'w') as f:
        json.dump(build_metadata(rows), f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
