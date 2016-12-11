import json
from watson_developer_cloud import PersonalityInsightsV3


def json_export(data, name):
    jsonFile = open(name + "_profile.json", "w")
    jsonFile.write(json.dumps(data, indent=4, separators=(',', ': ')))
    jsonFile.close()

if __name__ == "__main__":
    personality_insights = PersonalityInsightsV3(
        version='2016-12-10',
        username='e65927a0-94cc-4d27-b254-56e9d072e32d',
        password='FnaMoGx8mbp5')

    min_words = 100
    filename = 'EBay.json'
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

        if len(txt.split()) > min_words:
            profile = personality_insights.profile(
                txt.encode('utf8'), content_type='text/plain',
                raw_scores=True, consumption_preferences=True)
            profile['rating'] = review['rating']
            results.append(profile)
    json_export(results, filename)
