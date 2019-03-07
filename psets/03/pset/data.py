"""Data handling."""

import json
from .models import Museum


def load_data():
    """Read data from JSON and return a list of Museum objects."""
    museums = []
    with open('pset/data.json') as data_file:
        data = json.load(data_file)
        museums_dict = {}
        print('Importing museums:')
        for m in data['museums']:
            museum = Museum(
                m['id'],
                m['name'],
                m['latitude'],
                m['longitude'],
                N=1
            )
            museums_dict[m['id']] = museum
            print('\t✅[{}]'.format(museum.pk), museum.name)

        distances = []
        print('\nAdding edges:')
        for e in data['edges']:
            m1 = museums_dict[e['m1']]
            m2 = museums_dict[e['m2']]
            m1.connect_to(m2.pk, e['distance'])
            m2.connect_to(m1.pk, e['distance'])
            distances.append(e['distance'])
            print('\t🔗[{}] <---> [{}]'.format(m1.pk, m2.pk))

        L = sorted(distances)[1:]
        N = sum(L)
        print('\nAdding normalizer')
        print('\tComputed:', N)
        for m in museums_dict.values():
            m.N = N
            museums.append(m)

    return museums
