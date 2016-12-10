import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV3

"""
The example returns a JSON response whose content is the same as that in
   ../resources/personality-v3-expect2.txt
"""

personality_insights = PersonalityInsightsV3(
    version='2016-10-20',
    username='f869d757-c85d-4372-8df2-503f5b41d365',
    password='siUQ7mhItTJq')

with open(join(dirname(__file__), '../resources/personality.txt')) as profile_txt:
    profile = personality_insights.profile(
        profile_txt.read(), content_type='text/plain',
        raw_scores=True, consumption_preferences=True)

    print(json.dumps(profile, indent=2))
