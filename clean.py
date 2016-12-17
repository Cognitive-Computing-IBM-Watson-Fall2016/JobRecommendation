import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == "__main__":

    input_file = open('vectors.json').read()
    companies = json.loads(input_file)  # dict
    company_scores = []                 # list of 2-tuples

    user_file = open('person_tweet.json').read()
    user_vector = json.loads(user_file)['807677389878726657']
    user_vector = np.array(user_vector).reshape(1,-1)

    for company_name, company_vectors in companies.items():
        company_vectors = np.array(company_vectors)
        similarities = cosine_similarity(company_vectors, user_vector)
        company_score = 1 * similarities[0] + \
                        2 * similarities[1] + \
                        3 * similarities[2] + \
                        4 * similarities[3] + \
                        5 * similarities[4]
        company_scores.append((company_name, float(company_score)))

    company_scores.sort(key=lambda x: x[1])  # sort by score in descending order
    company_scores.reverse()

    print company_scores[0][0]
    print company_scores[1][0]
    print company_scores[2][0]
    print company_scores[3][0]
    #print company_scores[4][0]

