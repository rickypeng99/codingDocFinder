import sys
import http.client
import urllib
import json
import os
import re



def usage():
    print('dbFill.py -u <baseurl> -p <port> -n <numUsers> -t <numTasks>')

def main(argv):

     # Server Base URL and port
     baseurl = "localhost"
     port = 4000

     # Server to connect to (1: url, 2: port number)
     conn = http.client.HTTPConnection(baseurl, port)

     # HTTP Headers
     headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

     



     #uploading python tutorials 
     language = sys.argv[1]
     dirname = sys.argv[1] + "/"
     files = []
     wait = []
     #preventing 10.1 to be sorted before 2.1
     for root, dirs, filenames, in os.walk(dirname):
          for filename in sorted(filenames):
               if(filename[1] == "."):
                    files.append(filename)
               else:
                    wait.append(filename)
          
     for filename in wait:
          files.append(filename)

     #open all files
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
          
          #no code fragments for python tutorials
          codeFragment = "unidentified"    
          
          #print(title)
          #adding params
          params = urllib.parse.urlencode({'title': title, 'text': text, 'language': language, 'codeFragment': codeFragment})

          # POST
          conn.request("POST", "/api/fragments", params, headers)
          response = conn.getresponse()
          data = response.read()
          d = json.loads(data)
          if(d['data'] != "error"):
               print("Successfully uploaded " + title)
          else:
               #Some files from the java folder are empty, but that is fine.
               print("FAILED uploading " + title + d['message'])

     # Exit gracefully
     conn.close()
     print("Successfully uploaded all the fragments!")


if __name__ == "__main__":
     main(sys.argv[1:])
