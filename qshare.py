#!/usr/bin/env python3

import socketserver
import http.server
import argparse
import random
import string
import glob
import sys
import pdb
import os


class QuickShare(http.server.SimpleHTTPRequestHandler):

    def __init__(self, server, uri, filename):
        self.firstname = fname
        self.lastname = lname

    def do_GET(self):
        pdb.set_trace()
        referer = self.headers.get('Referer')
        if referer is None:
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("<html> <head><title> Hello World </title> </head> <body>", 'UTF-8'))
            images = glob.glob('*.jpg')
            rand = random.randint(0, len(images) - 1)
            filepath = images[rand]
            imagestring = "<img src = \"" + images[
                rand] + "\" height = 1028 width = 786 align = \"right\"/> </body> </html>"
            self.wfile.write(bytes(imagestring, 'UTF-8'))
        else:
            imgname = self.path
            print("Image requested is: ", imgname[1:])
            imgfile = open(imgname[1:], 'rb').read()
            self.send_header('Content-type', 'image/jpeg')
            self.send_header('Content-length', sys.getsizeof(imgfile))
            self.end_headers()
            self.wfile.write(imgfile)

    def serve_forever(port):
        print(path)
        print(server)
        socketserver.TCPServer(('', port), Server).serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Quick File Sharing')

    parser.add_argument(dest='filename',
                        help='file to share')
    parser.add_argument('-u', action='store', dest='uri',
                        default=''.join(random.choice(string.ascii_letters) for i in range(10)),
                        help='specify the uri link, default random')
    parser.add_argument('-s', action='store', dest='host',
                        default='0.0.0.0',
                        help='specify the host/ip, default 0.0.0.0')
    parser.add_argument('-p', action='store', dest='port',
                        default='0',
                        help='specify the port, default random')
    parser.add_argument('-t', action='store', dest='time',
                        type=int,
                        default=300,
                        help='specify how long we serve in seconds, default 300s')

    results = parser.parse_args()

    uri = results.uri
    host = results.host
    port = results.port
    server = ':'.join([host, port])

    filename = results.filename
    if not os.access(filename, os.R_OK):
        print("ERROR: Cannot read {0}".format(filename))
        sys.exit(1)

    #qshare = QuickShare

    #Server.serve_forever(8000)
