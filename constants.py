# Filenames to write output data.
LANGUAGES_FILENAME = 'languages.json'
METADATA_FILENAME = 'metadata.json'

# Keys of each type of register.
CORPUS_KEYS = [
    'corpus_path',
    'corpus_name',
    'domain',
    'provider',
    'license',
    'source',
    'languages',
    'parallel',
    'aggregated',
    'document_level',
    'third_parties',
    'publishable',
    'comments',
    'versions',
]
VERSION_KEYS = [
    'version_path',
    'version_name',
    'version_date',
    'states',
]
STATE_KEYS = [
    'state_path',
    'state_name',
    'encoding',
    'format',
    'state_date',
    'size_in_gigabytes',
    'size_in_million_tokens',
    'annotation_types',
    'annotation_format',
    'release_url',
    'prior_state',
    'actions',
    'script_location',
    'command',
    'action_comments',
    'email_address',
]

# Form fields that have checkbox type should be converted into lists of strings later.
LIST_KEYS = [
    'languages',
    'third_parties',
    'annotation_types',
    'actions',
]

# Attributes to display in search results.
DISPLAY_ATTRIBUTES = [
    'corpus_path',
    'corpus_name',
    'domain',
]
