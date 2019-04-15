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
     dirname = "python/"
     files = []
     wait = []
     #preventing 10.1 to be sorted before 2.1
     for root, dirs, filenames, in os.walk("python"):
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

          f = open(dirname + filename, 'r')
          text = f.read()

          #filtering out all chinese characters
          text = re.sub(u'[\u4e00-\u9fff]+','', text)
          #print(text)
          
          language = "python"
          #no code fragments for python tutorials
          codeFragment = "unidentified"    
          
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
               print("Failed uploading " + title)

     # Exit gracefully
     conn.close()
     print("Successfully uploaded all the fragments!")


if __name__ == "__main__":
     main(sys.argv[1:])
