import json
import numpy as np

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
            for item in facet['children'][0]['children']:
                person.append(item['percentage'])
        if facet['id'] == 'needs':
            for item in facet['children'][0]['children']:
                need.append(item['percentage'])
        if facet['id'] == 'values':
            for item in facet['children'][0]['children']:
                value.append(item['percentage'])
    X = need + person + value
    x = np.array(X)