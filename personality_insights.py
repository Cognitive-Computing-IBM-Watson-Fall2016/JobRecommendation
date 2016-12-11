import json
from watson_developer_cloud import PersonalityInsightsV3
from watson_developer_cloud import watson_developer_cloud_service

def json_export(data, name):
    jsonFile = open(name + "_profile.json", "w")
    jsonFile.write(json.dumps(data, indent=4, separators=(',', ': ')))
    jsonFile.close()

if __name__ == "__main__":
    personality_insights = PersonalityInsightsV3(
        version='2016-12-10',
        username='c53a4649-73dd-4960-af82-47681aa8637a',
        password='OnSSzjEwGRsF')
    max_input = 20
    min_words = 100
    filename = 'microsoft.json'
    input_file = open(filename).read()
    reviews = json.loads(input_file)
    results = []
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
        txt = txt + ' ' + txt
        if len(txt.split()) > min_words:
            try:
                profile = personality_insights.profile(
                    txt.encode('utf8'), content_type='text/plain',
                    raw_scores=True, consumption_preferences=True)
                profile['rating'] = review['rating']
                results.append(profile)
                if len(results) == max_input:
                    break
            except watson_developer_cloud_service.WatsonException:
                continue
    print filename, ' -- ', len(results)
    json_export(results, filename)
