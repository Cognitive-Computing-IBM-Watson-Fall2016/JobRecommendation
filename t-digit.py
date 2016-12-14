import json
import numpy as np
import pprint

if __name__ == "__main__":
    min_words = 100
    filename = 'test_data.json'
    input_file = open(filename).read()
    profile = json.loads(input_file)
    X = []
    y = []
    need = []
    value = []
    person = []
    for facet in profile['tree']['children']:
        if facet['id'] == 'personality':
            pprint.pprint()facet
            for item in facet['children']:
                person.append(item['percentage'])
        if facet['id'] == 'needs':
            for item in facet['children']:
                need.append(item['percentage'])
        if facet['id'] == 'values':
            for item in facet['children']:
                value.append(item['percentage'])
    X.append(need)
    X.append(person)
    X.append(value)
    print 'need', need
    print 'person', person
    print 'value', value
    print 'X', X
    x = np.array(X)
    print x