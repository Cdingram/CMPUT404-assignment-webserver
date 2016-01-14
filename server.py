#  coding: utf-8 
import SocketServer
from datetime import datetime
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        msg = self.data.split(' ')

        if msg[0] == 'GET':
            # requested file
            req = msg[1]
            #if it ends in /
            if req[-1] == '/':
                req += 'index.html'
            elif req == '/deep':
                req += '/index.html'
            if req in ['/index.html', '/base.css', '/deep/deep.css', '/deep/index.html']:
                try:
                    readFile = open('www'+req, 'r')
                    content = readFile.read()
                    readFile.close()
                except:
                    print('File Error')

                if req[-4:] == 'html':
                    mime = 'text/html'
                elif req[-3:] == 'css':
                    mime = 'text/css'
                else:
                    mime = 'text/plain'

                status = 'HTTP/1.1 200 OK\r\n'
                server = 'Server: Not a Server\r\n'
                date = 'Date: ' + str(datetime.now()) + '\r\n'
                mimeType = 'Content-Type: '+mime+'\r\n'
                length = 'Content-Length: '+str(len(content))+'\r\n'
                end = '\r\n'

                reply = status + server + date + mimeType + length + end + content

                self.request.send(reply)
            else:
                print '404'
                content = '''<!DOCTYPE html>
                    <html>
                    <body>
                    <h1>404 Error</h1>
                    <p>Webpage not found!! Sorry not today!</p>
                    </body>
                    </html>'''
                status = 'HTTP/1.1 404 Not Found'
                server = 'Server: Not a Server\r\n'
                date = 'Date: ' + str(datetime.now()) + '\r\n'
                mimeType = 'Content-Type: '+'text/html'+'\r\n'
                length = 'Content-Length: '+str(len(content))+'\r\n'
                end = '\r\n'

                reply = status + server + date + mimeType + length + end + content
                self.request.send(reply)

        else: 
            print 'not GET'





if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
