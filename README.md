# Corpora metadata

This is a project that aims to record and structure the metadata of the corpora stored at Data Transfer 1 (dt01.bsc.es:/gpfs/projects/bsc88/corpora).

TEMU's members and external collaborators should register each new corpus/version/state via this Google Form:
https://docs.google.com/forms/d/1D5BQc3hMKuOL6jrsNdICXeKga5iCRCjpMHrwR83LYDM

The responses of that form are stored in this Google Spreadsheet:
https://docs.google.com/spreadsheets/d/1M2BrRHwWmG4zclofFviPQrg9V67kNmx13GuK3od1jtw

## 0. Prepare the virtual environment

In a GNU/Linux or UNIX-based operating system, we can run all the following commands assuming that you have previously installed `git` and `python3` .

``` bash
$ git clone https://github.com/TeMU-BSC/corpora-metadata.git
$ cd corpora-metadata
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## 1. Create/update the metadata

The `updater.py` updates the `metadata.json` file (or creates it if it doesn't exist).

This script has been written using a `quickstart.py` script provided by Google as a starting point. It calls the Google Sheets API using a file named `credentials.json` which you should generate yourself:
https://developers.google.com/sheets/api/quickstart/python

``` bash
$ python updater.py
```

If it's the first time you run this script, you should allow 'Quickstart' to access your Google Spreadsheets.

After running it, an updated `metadata.json` file should be available in your current directory. Feel free to explore it, but the recommended way to do this by is using the `discoverer.py` and `finder.py` scripts explained in the next section.

## 2. Discover the search criteria

The `discoverer.py` script allows to know the available attributes to perform searches against the copora metadata. Run `python discoverer.py --help` to see the available arguments.

## 3. Find the corpora

The `finder.py` script can find either corpus and specific corpus states by some corpus-specific and/or state-specific attributes. Run `python finder.py --help` to see the available arguments.

## 4. Examples of use cases

* List all corpora

``` bash
$ python finder.py
```

* List all distinct third parties with access to some corpora

``` bash
$ python discoverer.py third_parties
```

* Find biomedical corpora

``` bash
$ python discoverer.py domain
$ python finder.py --domain biomedical
```

* Find parallel corpora in Catalan and Spanish

``` bash
$ python discoverer.py parallel
$ python discoverer.py languages
$ python finder.py --parallel yes --languages Catalan Spanish
```

Note that the search arguments are case-insensitive, so official capitalized 'Catalan' will find the same matches as lowercase 'catalan'.

Alternatively, you can use the ISO language codes (see `languages.json` ):

``` bash
$ python finder.py --parallel yes --languages ca es
```

Also note that every time you run the discoverer or the finder, the updater is called, so the metadata is always updated.
