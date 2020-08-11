# Corpora automated metadata

## Project Description

Automated metadata consists of two small Python scripts that, given a Google 
Form and a Google Spreadsheet on corpora metadata, create the necessary tools
to store and navigate throught the corpora records.

## Usage

### 0. Prepare virtual environment and test call to Google Sheets API v4

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
``` 

### 1. Create or update 'metadata.json'

```bash
$ python metadata_updater.py
``` 

### 2. Corpus Finder

The Corpus Finder can be used to search for corpora with specific characteristics: language, parallel, format, domain, 
projects... These may be extended in the future.

Run the following command:

```bash
$ # python corpus_finder.py --langs eu --parallel no --format txt --domain general --projects mt4all
$ python corpus_finder.py --parallel yes --format warc --domain general --third-parties mt4all

```
