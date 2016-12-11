import json
import numpy as np

if __name__ == "__main__":
    min_words = 100
    filename = 'EBay.json_profile.json'
    input_file = open(filename).read()
    profiles = json.loads(input_file)
    X = [] 
    y = []
    for profile in profiles:
        vector = []
        for need in profile['needs']:
            vector.append(need['percentile'])
        for value in profile['values']:
            vector.append(value['percentile'])
        for per in profile['personality']:
            vector.append(per['percentile'])
        for cp in profile['consumption_preferences']:
            if cp['consumption_preference_category_id'] == 'consumption_preferences_shopping':
                for temp in cp['consumption_preferences']:
                    if temp['consumption_preference_id'] == 'consumption_preferences_influence_utility':
                        vector.append(temp['score'])
                    if temp['consumption_preference_id'] == 'consumption_preferences_influence_online_ads':
                        vector.append(temp['score'])
                    if temp['consumption_preference_id'] == 'consumption_preferences_influence_social_media':
                        vector.append(temp['score'])
                    if temp['consumption_preference_id'] == 'consumption_preferences_influence_family_members':
                        vector.append(temp['score'])
                    if temp['consumption_preference_id'] == 'consumption_preferences_spur_of_moment':
                        vector.append(temp['score'])
                    if temp['consumption_preference_id'] == 'consumption_preferences_credit_card_payment':
                        vector.append(temp['score'])

            if cp['consumption_preference_category_id'] == 'consumption_preferences_health_and_activity':
                for temp in cp['consumption_preferences']:
                    vector.append(temp['score'])

            if cp['consumption_preference_category_id'] == 'consumption_preferences_environmental_concern':
                for temp in cp['consumption_preferences']:
                    vector.append(temp['score'])

            if cp['consumption_preference_category_id'] == 'consumption_preferences_entrepreneurship':
                for temp in cp['consumption_preferences']:
                    vector.append(temp['score'])

            if cp['consumption_preference_category_id'] == 'consumption_preferences_volunteering':
                for temp in cp['consumption_preferences']:
                    vector.append(temp['score'])
        X.append(vector)
        y.append(profile['rating'])

    X = np.array(X)
    y = np.array(y)

    print X
