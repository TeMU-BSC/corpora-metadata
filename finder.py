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
import pandas as pd

from constants import (METADATA_FILENAME,
                       CORPUS_KEYS, VERSION_KEYS, STATE_KEYS)


def parse_arguments() -> dict:
    '''Parse the command line and return a query object.'''
    parser = argparse.ArgumentParser(
        description='Find specific corpora by some metadata attributes.')

    # Corpus-specific arguments.
    parser.add_argument("--languages",
                        help="language ISO names, see 'languages.json' file", nargs='*')
    parser.add_argument("--domain",
                        help="knowledge area to which the corpus belongs")
    parser.add_argument("--third-parties",
                        help="entities that should have external access to this corpora", nargs='*')
    parser.add_argument("--provider",
                        help="entity that has provided the corpus")
    parser.add_argument("--parallel",
                        help="either the same data is present in more than one language")

    # TODO State-specific arguments.
    # parser.add_argument("--format",
    #                     help="format in which the corpus state is stored")
    # parser.add_argument("--annotation-types",
    #                     help="", nargs='*')
    # parser.add_argument("--actions",
    #                     help="", nargs='*')

    args = parser.parse_args()
    query = vars(args)
    return query


def get_matches(query: dict, metadata: List[dict]) -> list:
    '''Execute the query against the metadata.'''
    matches = metadata
    for k, v in query.items():
        if v:
            if isinstance(v, list):
                v_lower = [item.lower() for item in v]
                if k == 'languages':
                    v_lower = [language_name(item).lower() for item in v]
                matches = list(filter(lambda corpus: set(v_lower).issubset(
                    set([item.lower() for item in corpus.get(k)])), matches))
            elif isinstance(v, str):
                matches = list(filter(lambda corpus: v.lower()
                                      in corpus.get(k).lower(), matches))

    return matches


def to_tabular_format(matches: List[dict]) -> str:
    '''Convert the matches into tabular data format.
    Credit for panda's dataframe snippet: ona.degibert@bsc.es'''
    COLUMNS = [
        'CORPUS_PATH',
        'CORPUS_NAME',
        'DOMAIN',
        # 'PROVIDER'
    ]

    if len(matches) == 0:
        return "No matches found.\nTry 'python finder.py --help' for more information."

    results_df = pd.DataFrame(matches).iloc[:, 0:len(COLUMNS)]
    results_df.columns = COLUMNS
    results_df.set_index(pd.Series(range(1, len(matches) + 1)), inplace=True)
    return results_df


def main():
    '''Read the metadata file and run the query.'''
    with open(METADATA_FILENAME) as f:
        metadata = json.load(f)

    query = parse_arguments()
    matches = get_matches(query, metadata)
    tabular_results = to_tabular_format(matches)

    print(tabular_results)


if __name__ == '__main__':
    main()
