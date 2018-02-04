from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

from tfidf import event_title_cut
from collections import defaultdict

def csr_cosine(v1, v2):
    '''
    v1: csr_matrix
    v2: csr_matrix
    '''
    product = 0
    v1_norm = 0
    v2_norm = 0
    for same_index in set(v1.indices).intersection(set(v2.indices)):
        product += v1[0, same_index] * v2[0, same_index]
    if product == 0:
        return 0.0

    for v1_index in v1.indices:
        v1_norm += v1[0, v1_index] ** 2
    for v2_index in v2.indices:
        v2_norm += v2[0, v2_index] ** 2
    v1_norm = v1_norm ** 0.5
    v2_norm = v2_norm ** 0.5
    return product / (v1_norm * v2_norm)


event_title_tag_dict = event_title_cut('./data/eventsBefore20161231.data')
event_id_dict = defaultdict(int)
# corpus = [" ".join(item) for item in event_title_tag_dict.values()]
corpus = []
for index, item in enumerate(event_title_tag_dict.items()):
    corpus.append(" ".join(item[1]))
    event_id_dict[item[0]] = index

vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(corpus)
word_dict = vectorizer.vocabulary_
idf = vectorizer.idf_
print(tfidf.shape)

print('Test Train')
test_events_tag_dict = event_title_cut('./data/eventsAfter20161231.data')
test_vector_dict = defaultdict(dict)
i = 0
for train_event_id in event_id_dict.keys():
    i += 1
    if i == 100:
        break
    for test_event_id in test_events_tag_dict:
        if not test_vector_dict[test_event_id]:
            data = []
            col = []
            tags = test_events_tag_dict[test_event_id]
            for word in word_dict.keys():
                if word in tags:
                    data.append(tags.count(word) * idf[word_dict[word]])
                    col.append(word_dict[word])
            test_vector_dict[test_event_id] = {"data": data, "col": col, "row": [0] * len(col)}
        data = test_vector_dict[test_event_id]["data"]
        row = test_vector_dict[test_event_id]["row"]
        col = test_vector_dict[test_event_id]["col"]
        test_vector = csr_matrix((data, (row, col )), shape=(1, tfidf.shape[1]))
        cosine_similarity = csr_cosine(tfidf[event_id_dict[train_event_id]], test_vector)
        if cosine_similarity > 0.5:
            print(test_event_id, train_event_id)
