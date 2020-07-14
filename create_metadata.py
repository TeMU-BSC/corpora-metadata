import pandas as pd
import gspread
import json


def open_spreadsheet(sheet_name):
    # Edit your credentials and share the spreadsheet with your client_email from the credentials fle
    gc = gspread.service_account(filename='credentials.json')
    spreadsheet = gc.open("Metadata for MT4ALL")
    sheet = spreadsheet.worksheet(sheet_name)
    return sheet


def get_values(sheet_name, range_cells, drop_columns=list()):
    sheet = open_spreadsheet(sheet_name)
    data = sheet.get(range_cells)
    df = pd.DataFrame(data[1:], columns=data[0])
    df.drop(drop_columns, axis=1, inplace=True)
    df = df.apply(lambda x: x.astype(str).str.lower())
    return df

def get_actions(state_entry):
    actions = list()
    for index in range(int(len(state_entry) / 5)):
        index = str(index + 1)
        action_entry = dict()
        action_entry['name'] = state_entry['name_' + index]
        action_entry['src'] = state_entry['src_' + index]
        action_entry['tgt'] = state_entry['tgt_' + index]
        action_entry['script'] = state_entry['script_' + index]
        action_entry['order'] = state_entry['order_' + index]
        actions.append(action_entry)
    return actions


def get_corpus_version(version, date, path, size, publication):
    corpus_version = {'version': version, 'date': date, 'path': path, 'size': size, 'publication': publication}
    return (corpus_version)


def get_actions(state_entry):
    actions = []
    for index in range(int((len(state_entry) - 3) / 5)):  # remove three positions: corpus_version, name, date
        index = str(index + 1)
        action_entry = dict()
        action_entry['name'] = state_entry['name_' + index]
        action_entry['src'] = state_entry['src_' + index]
        action_entry['tgt'] = state_entry['tgt_' + index]
        action_entry['script'] = state_entry['script_' + index]
        action_entry['order'] = state_entry['order_' + index]
        actions.append(action_entry)
    return actions


def get_state(state_entry, version_path):
    new_path = version_path + '_' + state_entry['state_name'] + '_' + state_entry['date']
    clean_state_entry = dict(state=state_entry['state_name'], date=state_entry['date'], path=new_path,
                             prior_state=state_entry['prior_state'], release=state_entry['release'])
    actions = get_actions(state_entry)
    clean_state_entry['actions'] = actions
    return clean_state_entry

def get_languages(langs):
    langs_codes = dict(catalan='ca', english='en', spanish='es', basque='eu', finnish='fi', georgian='ka', kazah='kk',
             latvian='lv', ukrainan='uk')
    langs_list = []
    for language in langs.split(', '):
        langs_list.append(langs_codes[language])
    return(langs_list)

def process_corpora(entry):
    entry['corpus_versions'] = []
    entry['langs'] = get_languages(entry['langs'])
    path = entry['dir_name'] + '_' + entry['version']
    entry['projects'] = entry['projects'].split()
    entry['corpus_versions'].append(
        get_corpus_version(entry['version'], entry['date'], path, entry['size'], entry['publication']))
    entry.pop('version')
    entry.pop('date')
    entry.pop('size')
    entry.pop('publication')
    return entry


def main():
    corpora = get_values('Corpora', 'B:T')
    versions = get_values('Corpus versions', 'T:X')
    states = get_values('States', 'Y:AQ')
    dict_corpora = corpora.to_dict(orient='records')
    dict_versions = versions.to_dict(orient='records')
    dict_states = states.to_dict(orient='records')

    data_to_write = {}
    # Process corpora sheet
    for c_entry in dict_corpora:
        c_entry = process_corpora(c_entry)

        # Process corpus versions sheet
        for v_entry in dict_versions:
            if v_entry['pretty_name'] == c_entry['pretty_name']:
                # Process corpus states sheet
                path = c_entry['dir_name'] + '_' + v_entry['version']
                c_entry['corpus_versions'].append(
                    get_corpus_version(v_entry['version'], v_entry['date'], path, v_entry['size'],
                                       v_entry['publication']))

    # Now that all corpus versions have been appended
    for corpus_data in dict_corpora:
        for version_data in corpus_data['corpus_versions']:
            corpus_version = corpus_data['pretty_name'] + ' ' + version_data['version']
            path = corpus_data['dir_name'] + '_' + version_data['version']
            states_list = []
            for s_entry in dict_states:
                # Fix date format
                date = s_entry['date']
                if "/" in date:
                    s_entry['date'] = date[-4:] + date[3:5] + date[:2]
                # Remove None values
                s_entry = {k: v for k, v in s_entry.items() if v != 'none'}
                if s_entry[
                    'corpus_version'] == corpus_version:
                    states_list.append(get_state(s_entry, path))
                version_data['corpus_version_states'] = states_list

    with open('metadata.json', 'w', encoding='utf-8') as metadata:
        json.dump(dict_corpora, metadata, indent=4, ensure_ascii=False)


main()
