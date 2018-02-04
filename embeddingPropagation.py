import subprocess
from collections import defaultdict
from functools import reduce

def vector_add(v1, v2):
    result = []
    for a, b in zip(v1, v2):
        if type(a) != float:
            a = float(a)
        if type(b) != float:
            b = float(b)
        result.append(a + b)
    return result


embedding_dict = defaultdict(list)
with open('./data/rep.hpe', 'rt') as fin:
    fin.readline()
    for line in fin:
        vertex, *embedding = line.split()
        embedding_dict[vertex] = embedding

fout = open('seriesEventEmbeddingAll.data', 'wt')
command = "awk '{print $1}' seriesGraphAll.data"
test_event_id_list = subprocess.check_output(command, shell=True).split()
for test_event_id in set(test_event_id_list):
    test_event_id = test_event_id.decode('utf-8')
    command = "awk \'{if(\"%s\"==$1){print $2} }\' \'./seriesGraphAll.data\'" % test_event_id
    related_event_list = subprocess.check_output(command, shell=True).split()
    related_embedding_list = []
    for event in related_event_list:
        event = event.decode('utf-8')
        related_embedding_list.append(embedding_dict[event])
    fout.write("%s " %test_event_id)
    length = len(related_embedding_list)
    # print(related_embedding_list)
    for number in reduce(vector_add, related_embedding_list):
        fout.write('%f ' % (float(number)/length))
    fout.write('\n')
fout.close()
