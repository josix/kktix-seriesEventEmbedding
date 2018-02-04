import subprocess
import jieba
import jieba.analyse

command = "awk -F, '{print $1}' ../preproecessed_data/eventNameList.data"
id_list = subprocess.check_output(command, shell=True).decode('utf-8').split('\n')
command = "awk -F, '{print $2}' ../preproecessed_data/eventNameList.data"
events = subprocess.check_output(command, shell=True).decode('utf-8').split('\n')

jieba.set_dictionary("./jieba-zh_TW/jieba/dict.txt")

for id_number, title in zip(id_list, events):
    tags = jieba.analyse.extract_tags(title)
    print(id_number," / ".join(tags), sep=",")
