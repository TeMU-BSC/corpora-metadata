'''
Discover the search criteria to properly find corpora in 'metadata.json'.
That corpora is placed at Data Transfer 1 (dt01.bsc.es:/gpfs/projects/bsc88/corpora).

Author: alejandro.asensio@bsc.es
'''

import argparse
import json
from typing import List

from iso_language_codes import language, language_name
import pandas as pd

from constants import (
    METADATA_FILENAME,
    CORPUS_KEYS, VERSION_KEYS, STATE_KEYS,
    DISPLAY_ATTRIBUTES
)

import updater


def parse_attribute() -> dict:
    '''Parse the command line and return the attribute name.'''
    parser = argparse.ArgumentParser(
        description='List all available values for a specific corpus attribute.')

    # Corpus-specific arguments.
    parser.add_argument("attribute",
                        help="key name in every corpus object in 'metadata.json' file")

    # TODO State-specific arguments.

    args = parser.parse_args()
    return args.attribute


def get_distinct_values(attribute: str, metadata: List[dict]) -> list:
    '''Return the distinct unique values for the given attribute.'''
    values = list()
    for corpus in metadata:
        value = corpus.get(attribute)
        if isinstance(value, list):
            values.extend(value)
        else:
            values.append(value)
    non_empty_values = [value for value in values if value]
    distinct_values = set(non_empty_values)
    return distinct_values


def to_tabular_format(attribute: str, values: List[dict]) -> str:
    '''Convert the values into one-column tabular data format.
    Credit for panda's dataframe snippet: ona.degibert@bsc.es'''
    columns = [attribute.upper()]

    if len(values) == 0:
        return "No values found.\nTry 'python discoverer.py --help' for more information."

    results_df = pd.DataFrame(values).iloc[:, 0:len(columns)]
    results_df.columns = columns
    results_df.set_index(pd.Series(range(1, len(values) + 1)), inplace=True)
    return results_df


def main():
    '''Read the metadata file and run the query.'''
    with open(METADATA_FILENAME) as f:
        metadata = json.load(f)

    attribute = parse_attribute()
    values = get_distinct_values(attribute, metadata)
    tabular_results = to_tabular_format(attribute, values)

    print(tabular_results)


if __name__ == '__main__':
    updater.main()
    main()
