import jieba
import jieba.analyse

from collections import defaultdict
import time

def cosine(v1, v2):
    product = 0
    v1_norm = 0
    v2_norm = 0
    for a, b in zip(v1, v2):
        if a == 0 and b == 0:
            continue
        elif a == 0:
            v2_norm += b * b
            continue
        elif b == 0:
            v1_norm += a * a
            continue
        product += a * b
        v1_norm += a * a
        v2_norm += b * b
    v1_norm = v1_norm ** 0.5
    v2_norm = v2_norm ** 0.5
    return product/(v1_norm * v2_norm)

def event_title_cut(filepath):
    event_title_tag_dict = defaultdict(list)
    jieba.set_dictionary("./jieba-zh_TW/jieba/dict.txt")
    with open(filepath, 'rt') as fin:
        for line in fin:
            event_id, event_type, event_title, *temp = line.strip().split(',')
            event_title_tag_dict[int(event_id)] = jieba.analyse.extract_tags(event_title)
    return event_title_tag_dict

if __name__ == "__main__":
    from sklearn import feature_extraction
    from sklearn.feature_extraction.text import TfidfVectorizer

    start = time.time()
    corpus = []
    event_dict = defaultdict(str)
    id_dict = defaultdict(int)
    with open('./data/tfidf/eventTitleTagsList.data', 'rt') as fin:
        i = 0
        for line in fin:
            id_number, tags = line.strip().split(',')
            if not id_number:
                continue
            event_dict[i] = line.strip()
            id_dict[i] = int(id_number)
            corpus.append(tags.replace(' / ', " "))
            i += 1
        print(corpus[:10])

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus)
    print(tfidf.shape)

    fout = open('temp', 'wt')
    series_out = open('SeriesEvents.data', 'wt')
    words = vectorizer.get_feature_names()
    for i in range(len(corpus)):
        fout.write('\n----Document %s----\n' % event_dict[i])
        v1 = tfidf[i].toarray()[0]
        series_list = []
        for j in range(len(corpus)):
            v2 = tfidf[j].toarray()[0]
            cosine_similarity = cosine(v1, v2)
            if cosine_similarity > 0.5:
                fout.write('%s\n' % event_dict[j])
                series_list.append((cosine_similarity, id_dict[j]))
        if len(series_list) == 1:
            continue
        series_out.write('%d' % id_dict[i])
        series_list.sort(reverse=True)
        for event in series_list:
            series_out.write(',%d' % event[1])
        series_out.write('\n')
        if i == 1000:
            break

    end = time.time()
    print(end - start)
   #dictionary = corpora.Dictionary(corpus)
   #dictionary.save('./eventTitleDict.dict')

   #print(tfidf["風雲榜"])
