import os
import re
import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import http.client
import urllib





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
    return all_text, files

def get_ctext():
    data = json.load(open("c_lib/c_lib.json"))
    text = []
    filenames = []
    for doc in data:
        text.append(doc["Text"])
        filenames.append(doc['Title'])
    return text, filenames






def get_id(conn, filenames, similar_array, index):
    ids = []
    for i in range(0, len(similar_array[index])):

        name = filenames[similar_array[index][i]].replace(" ", "%20")

        conn.request("GET","/api/search/" + name)

        response = conn.getresponse()
        data = response.read()
        d = json.loads(data)
        ids.append(str(d['data'][0]['_id']))

    return ids


def main(argv):


        #SERVER PART

    # Server Base URL and port
    baseurl = "localhost"
    port = 4000

    # Server to connect to (1: url, 2: port number)
    conn = http.client.HTTPConnection(baseurl, port)

    # HTTP Headers
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}



    language = sys.argv[1]
    if language == "c":
        text, filenames = get_ctext()
    else:
        text, filenames = get_text1(language)
    tfidf = TfidfVectorizer(input='content',analyzer='word', min_df = 0, stop_words = 'english').fit_transform(text)
    similar_list = []
    for i in range(tfidf.shape[0]):
        similar_list.append(find_similar(tfidf, i))
    count = len(similar_list)
    print("Successfully match for "+ str(count) + " docs")
    print("original" + filenames[1])
    ids = []
    ids = get_id(conn, filenames, similar_list, 1)
    for i in range(0, len(similar_list[1])):
        print("similar: " + filenames[similar_list[1][i]])


        print("similar id: " + ids[i])
    # Exit gracefully
    conn.close()
if __name__ == "__main__":
     main(sys.argv[1:])
