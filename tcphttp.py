import httplib
import base64
import string
import random
def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
def random_generator20(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
from HTMLParser import HTMLParser
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.record=True
    def handle_endtag(self, tag):
        self.record=False
    def handle_data(self, data):
        if self.record:
            self.resp=data
# instantiate the parser and fed it some HTML

parser = MyHTMLParser()
parser.record=False
parser.resp=""

##ARGPARSE
import argparse
parserarg = argparse.ArgumentParser(description="Client of Tor2TCP")
parserarg.add_argument('-r','--remote', help='url of host ex. *.onion.to', required=True)
parserarg.add_argument('-l','--listenport', help='TCP port to listen on the local host ex. 10000', required=True)
args = vars(parserarg.parse_args())

import socket

#TODO make these arguments??? -> dynamic 
TCP_IP = '127.0.0.1'
TCP_PORT = int(args["listenport"])
BUFFER_SIZE = 1024*8 #8 gaat? safer is lower Normally 1024, but we want fast response


## TODO HERE IS PROBLEM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

def listen():
    s.listen(1)
    global conn
    global addr
    conn, addr = s.accept()
    global connection_dead
    connection_dead=False
    print 'Connection address:', addr
    global ID
    ID = random_generator20()

listen()

###HTTP
http_conn = httplib.HTTPSConnection(args["remote"])
try:
    while 1:#infinite
            #test if still alive
            try:
                conn.send("")#test this??
            except:
                pass
                connection_dead=True

            if connection_dead:
                listen()

            data = ""
            conn.settimeout(0.6)
            try:
                data = conn.recv(BUFFER_SIZE)
            except:
                pass
            if len(data) != 0:
                encoded = base64.b64encode(data)
            else:
                encoded = ""
            #SEND HTTP REQUEST BACK
            http_conn.request("GET", "/"+random_generator()+"/ID/"+ID+"/"+encoded)
            #RETRIEVE DATA
            r1 = http_conn.getresponse()
            data1 = r1.read()#data1 is the full html page
            parser.resp=""
            parser.feed(data1)
            
            #TODO EVERY RECV EN send IN TEST FOR CONNECTION OUT
            if len(parser.resp) != 0:
                try:
                    response=base64.b64decode(parser.resp)
                except:
                    response = ""
                    pass 
                try:
                    conn.send(response)  # send response
                except:
                    pass
                    connection_dead=True
            
except:
    raise
    pass
s.close()
conn.close() #close
#TODO when close??? keyboardexception of quit?
http_conn.close()
