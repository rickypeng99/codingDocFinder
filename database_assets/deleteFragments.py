import sys
import getopt
import http.client
import urllib
import json


def getFragments(conn):
    #Retrieve every fragment

    conn.request("GET","/api/fragments?query=all&language=all")
    response = conn.getresponse()
    data = response.read()
    d = json.loads(data)

    fragments = []
    for i in range(0, len(d['data'])):
        fragments.append(str(d['data'][i]['_id']))
    return fragments

def main(argv):
    # Server Base URL and port
    baseurl = "localhost"
    port = 4000

    # Server to connect to (1: url, 2: port number)
    conn = http.client.HTTPConnection(baseurl, port)

    fragments = getFragments(conn)

    for fragment in fragments:
        conn.request("DELETE","/api/fragments/"+fragment)
        response = conn.getresponse()
        data = response.read()


    # Exit gracefully
    conn.close()
    print("All fragments removed at "+baseurl+":"+str(port))

if __name__ == "__main__":
     main(sys.argv[1:])
