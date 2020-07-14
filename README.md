# README
## Project Description
Automated metadata consists of two small Pythons scripts that, given a Google 
Form and a Google Spreadsheet on corpora metadata, create the necessary tools to store and navigate throught the
corpora records.

## Usage
### 1. Create 'metadata.json'
To create the 'metadata.json', you'll need a Google Spreadsheets API. 

Go to google.sheets and enable the API, create service account credentials and save them in a file called 'credentials.json'.
Share the document you want to read from with your client_email, extracted from the credentials file.

Run the following command: 
```
$ python3 create_metadata.py
```
### 2. Corpus Finder
The Corpus Finder can be used to search for corpora with specific characteristics: language, parallel, format, domain,
projects... These may be extended in the future.

Run the following command:
```
$ python3 corpus_finder.py --langs eu --parallel no --format txt --domain general --projects mt4all
```
