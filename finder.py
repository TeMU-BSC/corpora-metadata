'''
Find corpora in Data Transfer 1 (dt01.bsc.es:/gpfs/projects/bsc88/corpora)
reading the 'metadata.json' file and querying through the command line by
some corpus attributes.

Author: alejandro.asensio@bsc.es
'''

import argparse
import json
from typing import List

from iso_language_codes import language, language_name
from pandas import DataFrame

from constants import (
    RESPONSES_FILENAME, METADATA_FILENAME,
    CORPUS_KEYS, VERSION_KEYS, STATE_KEYS,
    LIST_KEYS,
    DISPLAY_ATTRIBUTES,
)

import updater


def parse_arguments() -> dict:
    '''Parse the command line and return a query object.'''
    parser = argparse.ArgumentParser(description='Find specific corpora by some metadata attributes.')

    # Corpus-level arguments.
    parser.add_argument("--languages", help="language ISO names, see 'languages.json' file", nargs='*')
    parser.add_argument("--third-parties", help="entities that should have external access to this corpora", nargs='*')
    parser.add_argument("--domain", help="knowledge area to which the corpus belongs")
    parser.add_argument("--provider", help="entity that has provided the corpus")
    parser.add_argument("--parallel", help="[yes/no] - either the same data is present in more than one language")
    parser.add_argument("--aggregated", help="[yes/no] - either the corpus is built from the addition of other previous corpora")
    parser.add_argument("--document-level", help="[yes/no] - either the corpus is parseable by document")
    parser.add_argument("--publishable", help="[yes/no/na] - either the corpus is publishable or not. NA stands for Not Applicable (the person who registered the corpus doesn't know if it is publishable)")

    # State-level arguments.
    parser.add_argument("--actions", help="steps applied to an existing corpus state", nargs='*')
    parser.add_argument("--annotation-types", help="types of annotation that the corpus holds", nargs='*')
    parser.add_argument("--encoding", help="encoding type")
    parser.add_argument("--format", help="format in which the corpus state is stored")
    parser.add_argument("--email-address", help="person who registered this corpus state")

    args = parser.parse_args()
    query = vars(args)
    return query


def get_matches(query: dict, responses: List[dict]) -> list:
    '''Execute the query against the responses from the google form.'''
    matches = responses
    query_items = [(k, v) for k, v in query.items() if v]
    for k, v in query_items:
        if k in LIST_KEYS:
            v_lower = [item.lower() for item in v]
            if k == 'languages':
                v_lower = [language_name(item).lower() for item in v]
            matches = list(filter(lambda response: set(v_lower).issubset(set([item.lower() for item in (response.get(k).split(', ') if response.get(k) else [])])), matches))
        else:
            if k == 'publishable' and v == 'na':
                v = "I don't know"
            matches = list(filter(lambda response: v.lower() in (response.get(k).lower() if response.get(k) else ''), matches))

    return matches


def to_tabular_format(matches: List[dict]) -> str:
    '''Convert the matches into tabular data format.
    Credit for panda's dataframe snippet: ona.degibert@bsc.es'''
    if len(matches) == 0:
        return "No matches found.\nTry 'python finder.py --help' for more information."

    df = DataFrame(matches, index=range(1, len(matches) + 1), columns=DISPLAY_ATTRIBUTES)
    return df


def main():
    '''Read the metadata file and run the query.'''
    query = parse_arguments()
    
    # with open(METADATA_FILENAME) as f:
    #     metadata = json.load(f)
    # matches = get_matches(query, metadata)
    
    with open(RESPONSES_FILENAME) as f:
        responses = json.load(f)
    matches = get_matches(query, responses)

    tabular_results = to_tabular_format(matches)

    print(tabular_results)


if __name__ == '__main__':
    updater.main()
    main()
