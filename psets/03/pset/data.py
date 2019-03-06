"""Data handling."""

import json


def load_data():
    """Read data from JSON and return a list of Museum objects."""
    museums = []
    with open('pset/data.json') as data_file:
        data = json.load(data_file)
        for m in data['museums']:
            print(m, '\n**********')
    return museums
