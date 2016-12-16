import json
from watson_developer_cloud import PersonalityInsightsV3
from watson_developer_cloud import watson_developer_cloud_service
import pprint
min_words = 100


def json_export(data):
    jsonFile = open("data_analyzed.json", "w")
    jsonFile.write(json.dumps(data, indent=4, separators=(',', ': ')))
    jsonFile.close()


def to_vector(profile):
    need_val = []
    value_val = []
    person_val = []
    for need in profile['needs']:
        need_val.append(need['percentile'])
    for values in profile['values']:
        value_val.append(values['percentile'])
    for per in profile['personality']:
        person_val.append(per['percentile'])
    X = need_val + value_val + person_val
    return X


def get_personality(summ):
    personality_insights = PersonalityInsightsV3(
        version='2016-12-10',
        username='c53a4649-73dd-4960-af82-47681aa8637a',
        password='OnSSzjEwGRsF')
    result = []
    for i in range(0, 5):
        txt = summ[i]
        if len(txt.split()) > min_words:
            try:
                profile = personality_insights.profile(
                    txt.encode('utf8'), content_type='text/plain',
                    raw_scores=True, consumption_preferences=True)
                result.append(to_vector(profile))
            except watson_developer_cloud_service.WatsonException:
                continue
        else:
            result.append([])
    return result


def classify_review(com):
    input_file = open(com + '.json').read()
    reviews = json.loads(input_file)
    result = []
    for i in range(0,5):
        result.append('')
    for review in reviews:
        txt = ''
        if review['advice'] != None:
            txt += review['advice']
        if review['cons'] != None:
            txt += review['cons']
        if review['pros'] != None:
            txt += review['pros']
        if review['summary'] != None:
            txt += review['summary']
        result[review['rating'] - 1] += txt
    return result

if __name__ == "__main__":
    min_words = 100
    companies = ['Citi']
    dict = {}
    for company in companies:
        temp = classify_review(company)
        vector = get_personality(temp)
        dict.update({company : vector})
    json_export(dict)