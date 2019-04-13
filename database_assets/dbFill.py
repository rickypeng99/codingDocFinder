#!/usr/bin/env python

"""
 * @file dbFill.py
 * Used in CS498RK MP4 to populate database with randomly generated users and tasks.
 *
 * @author Aswin Sivaraman
 * @date Created: Spring 2015
 * @date Modified: Spring 2015
 * @date Modified: Spring 2019
"""

import sys
import getopt
import http.client
import urllib
import json
from random import randint
from random import choice
from datetime import date
from time import mktime

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
    
    title = "3.1.3 Lists"
    
    #text
    f = open('3.1.3. Lists','r')
    text = f.read()

    language = "python"

    codeFragment = ""    
    
    params = urllib.parse.urlencode({'title': title, 'text': text, 'language': language, 'codeFragment': codeFragment})

    # POST
    conn.request("POST", "/api/fragments", params, headers)
    response = conn.getresponse()
    data = response.read()
    d = json.loads(data)

    # Exit gracefully
    conn.close()
    print("successfully uploaded " + title)


if __name__ == "__main__":
     main(sys.argv[1:])
