import json
from watson_developer_cloud import PersonalityInsightsV3

min_words = 100


def json_export(data):
    jsonFile = open("data_analyzed_1.json", "w")
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


def get_personality(rev):
    personality_insights = PersonalityInsightsV3(
        version='2016-12-10',
        username='c53a4649-73dd-4960-af82-47681aa8637a',
        password='OnSSzjEwGRsF')
    result = []
    for txt in rev:
        profile = personality_insights.profile(
            txt.encode('utf8'), content_type='text/plain',
            raw_scores=True, consumption_preferences=True)
        result.append(to_vector(profile))
    return result


def classify_review(com):
    result = []
    for i in range(0,5):
        input_file = open('./data/' + com + '_' + str(i+1) + '.json').read()
        reviews = json.loads(input_file)
        txt = ''
        for review in reviews:
            if review['advice'] != None:
                txt += '' + review['advice']
            if review['cons'] != None:
                txt += '' + review['cons']
            if review['pros'] != None:
                txt += '' + review['pros']
            if review['summary'] != None:
                txt += '' + review['summary']
        result.append(txt)
    return result

if __name__ == "__main__":
    companies = ['Facebook', 'Google', 'LinkedIn']
    dict = {}
    for company in companies:
        temp = classify_review(company)
        vector = get_personality(temp)
        dict.update({company: vector})
    json_export(dict)
