# Corpora metadata

This is a project that aims to record and structure the metadata of the corpora stored at Data Transfer 1 (dt01.bsc.es).

TEMU's members and external collborators should register each new corpus/version/state via this Google Form:
https://docs.google.com/forms/d/1D5BQc3hMKuOL6jrsNdICXeKga5iCRCjpMHrwR83LYDM

The responses of that form are stored in this Google Spreadsheet:
https://docs.google.com/spreadsheets/d/1M2BrRHwWmG4zclofFviPQrg9V67kNmx13GuK3od1jtw

## Usage

### 0. Prepare the virtual environment

``` bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### 1. Update the metadata

The `updater.py` updates the `metadata.json` file (or creates it if it doesn't exist).

This script has been written using `quickstart.py` as a starting point. It calls the Google Sheets API using a file named `credentials.json` which you should generate yourself:
https://developers.google.com/sheets/api/quickstart/python

``` bash
$ python updater.py
```

If it's the first time you run this script, you should allow 'Quickstart' to access your Google Spreadsheets.

### 2. Discover the corpora

``` bash
$ python discoverer.py
$ python discoverer.py --languages --domains
$ python discoverer.py --formats
```

### 3. Find corpora

The `finder.py` script can find specific corpus states by some attributes. Run `python finder.py --help` to see the list of search attributes.

``` bash
$ python finder.py --languages ca es --parallel yes --format warc --domain general --third-parties mt4all
```
