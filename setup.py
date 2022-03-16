import json

import setuptools

with open(file="pyrcs/data/metadata.json", mode='r') as metadata_file:
    metadata = json.load(metadata_file)

__package__, __version__ = metadata['Package'], metadata['Version']

__home_page__ = 'https://github.com/mikeqfu/' + f'{__package__}'

setuptools.setup(
    name=__package__,
    version=__version__,
    description=metadata['Description'],
    url=__home_page__,
    author=metadata['Author'],
    author_email=metadata['Email'],
    keywords=[
        'Python', 'Railway Codes', 'Railway', 'Bridges', 'CRS', 'NLC', 'TIPLOC',
        'STANOX', 'Electrification', 'ELR', 'Mileage', 'LOR', 'Stations',
        'Signal boxes', 'Tunnels', 'Viaducts', 'Depots', 'Tracks',
    ],
    project_urls={
        'Documentation': f'https://{__package__}.readthedocs.io/en/{__version__}/',
        'Source': __home_page__,
        'Bug Tracker': __home_page__ + '/issues',
    },
)
