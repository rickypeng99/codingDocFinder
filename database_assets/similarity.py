import os
import re
import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def find_similar(tfidf, index):
    cos_simi = linear_kernel(tfidf[index:index+1], tfidf).flatten()
    re = []
    count = 0

    for i in cos_simi.argsort()[::-1]:
        if count == 1 and i != index:
            print(cos_simi[i], i)
            re.append(i)
            count += 1
            continue
        if count < 5 and cos_simi[i] > 0.3:
            print(cos_simi[i], i)
            if i != index:
                re.append(i)
        else:
            break
        count += 1
    return re

def get_text1(language):
    dirname = language + "/"
    files = []
    wait = []
    all_text = []
    for root, dirs, filenames, in os.walk(dirname):
        for filename in sorted(filenames):
            if(filename[1] == "."):
                files.append(filename)
            else:
                wait.append(filename)
        for filename in wait:
            files.append(filename)

        for filename in files:
            title = filename
            if(language == "python"):
                f = open(dirname + filename, 'r', encoding='gbk')
                text = f.read()
            else:
                f = open(dirname + filename, 'r', encoding='utf-8')
                text = f.read()
            #filtering out all chinese characters
            text = re.sub(u'[\u4e00-\u9fff]+','', text)
            all_text.append(text)
    return all_text

def get_ctext():
    data = json.load(open("c_lib/c_lib.json"))
    text = []
    for doc in data:
        text.append(doc["Text"])
    return text
def main(argv):
    language = sys.argv[1]
    if language == "c":
        text = get_ctext()
    else:
        text = get_text1(language)
    tfidf = TfidfVectorizer(input='content',analyzer='word', min_df = 0, stop_words = 'english').fit_transform(text)
    similar_list = []
    for i in range(tfidf.shape[0]):
        similar_list.append(find_similar(tfidf, i))
    count = len(similar_list)
    print("Successfully match for "+ str(count) + " docs")

if __name__ == "__main__":
     main(sys.argv[1:])
