import json
import optparse
import pandas as pd

def parse_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-l','--langs', action="store", default=False)
    parser.add_option('-p','--parallel', action="store", default=False)
    parser.add_option('-f','--format', action="store", default=False)
    parser.add_option('-d','--domain', action="store", default=False)
    parser.add_option('-j','--projects', action="store", default=False)
    options, args = parser.parse_args()

    query = dict()
    for opt, value in options.__dict__.items():
        if value is not False:
            query[opt]=value
    return query

def main():
    metadata = json.loads(open ('metadata.json').read())
    query = parse_arguments()
    all_matches = list()
    for query_item in query:
        if query_item == 'lang' or 'projects':
            match = list(filter(lambda x: query[query_item] in x[query_item], metadata))
        else:
            match = list(filter(lambda x: x[query_item] == query[query_item], metadata))

        all_matches.extend(match)

    results = list()
    for match in all_matches:
        if all_matches.count(match) == len(query) and match not in results:
            results.append(match)
    if len(results) == 0:
        results = "No results found, please, try again with a new query"
    else:
        results_df = pd.DataFrame(results).iloc[:, 0:2]
        results_df.columns = results_df.columns.str.upper()
        results_df = results_df.shift()[1:]
        results = results_df
    #results = [x for n, x in enumerate(all_matches) if x in all_matches[:n]]
    print(results) #Decide which columns to return


main()