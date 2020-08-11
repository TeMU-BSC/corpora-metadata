'''
Update the 'metadata.json' file for TEMU's corpora.

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
from typing import Optional, Sequence

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from iso_language_codes import language, language_name, language_dictionary


@dataclass
class State:
    state_path: str
    state_name: str
    encoding: str
    format: str
    state_date: str
    size_in_gigabytes: Optional[str] = None
    size_in_million_tokens: Optional[str] = None
    annotation_types: Optional[Sequence[str]] = None
    annotation_format: Optional[str] = None
    release_url: Optional[str] = None
    prior_state: Optional[str] = None
    actions: Optional[Sequence[str]] = None
    script_location: Optional[str] = None
    command: Optional[str] = None
    action_comments: Optional[str] = None


@dataclass
class Version:
    version_path: str
    version_name: str
    version_date: str
    states: Sequence[State]


@dataclass
class Corpus:
    corpus_path: str
    corpus_name: str
    source: str
    provider: str
    languages: Sequence[str]
    parallel: str
    domain: str
    document_level: str
    third_parties: Sequence[str]
    license: str
    publishable: str
    comments: Optional[str] = None
    versions: Sequence[Version]


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a spreadsheet.
SPREADSHEET_ID = '1M2BrRHwWmG4zclofFviPQrg9V67kNmx13GuK3od1jtw'
RANGE_NAME = 'Answers!A1:AI'

# Save language codes and names into a json file.
# open('languages.json', 'w').write(json.dumps(language_dictionary(), ensure_ascii=False, sort_keys=True, indent=4))

# List of the form fields with checkbox type.
CHECKBOX_FIELDS = ['languages', 'third_parties', 'annotation_types', 'actions']
# BOOLEAN_FIELDS = ['parallel', 'document_level']


def to_snake_case(input: str) -> str:
    return input.replace(' ', '_').lower()


def language_code(language_name: str) -> str:
    '''Return the language code for a given language name.'''
    for code, info in language_dictionary().items():
        if info.get('Name') == language_name:
            return code


def from_checkboxes_to_list(checkboxes: str) -> Sequence[str]:
    '''Convert some words separated by comma and whitespace (', ') into a list of strings.'''
    return checkboxes.split(', ')


def set_state():
    '''Build the state structure.'''
    state_keys = ['state_path', 'state_name', 'encoding', 'format', 'state_date', 'size_in_gigabytes', 'size_in_million_tokens',
                  'annotation_types', 'annotation_format', 'release_url', 'prior_state', 'actions', 'script_location', 'command', 'action_comments']


def set_version():
    '''Build the version structure.'''
    version_keys = ['version_path', 'version_name', 'version_date', 'states']


def set_corpus():
    '''Build the corpus structure.'''
    corpus_keys = ['corpus_path', 'corpus_name', 'source', 'provider', 'languages', 'parallel',
                   'domain', 'document_level', 'third_parties', 'license', 'publishable', 'comments', 'versions']


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

    # Process the data inside the spreadsheet
    questions = values[0]
    responses = values[1:]
    questions[0] = 'timestamp'
    questions[2] = 'email_address'
    keys = [to_snake_case(question) for question in questions]
    # print(keys)

    responses = [dict(zip(keys, response)) for response in responses]

    # Save the raw responses into a json file.
    open('responses.json', 'w').write(json.dumps(
        responses, ensure_ascii=False, indent=4))

    for response in responses:

        # Convert checkbox fields into lists.
        for k, v in response.items():
            if k in CHECKBOX_FIELDS:
                response[k] = from_checkboxes_to_list(v)

        # Organize nested versions and states fields
        if response.get('i_want_to_register_a_new:') == 'Corpus':
            corpus = Corpus(
                corpus_path=response.get('corpus_path'),
                corpus_name=response.get('corpus_name'),
                source=response.get('source'),
                # ...
            )
        elif response.get('i_want_to_register_a_new:') == 'Version':
            # TODO Search for the corresponding corpus_path in version_path
            print('version...')

        elif response.get('i_want_to_register_a_new:') == 'State':
            # TODO Search for the corresponding version_path in state_path
            print('state...')

    # Save processed responses into the final 'metadata.json' file.
    open('metadata.json', 'w').write(json.dumps(
        responses, ensure_ascii=False, indent=4))

    # TESTING
    version = Version(version_path='/fake/path', version_name='Fake Name',
                      version_date='dd/mm/yyyy', states=[{}])
    print(vars(version))


if __name__ == '__main__':
    main()
