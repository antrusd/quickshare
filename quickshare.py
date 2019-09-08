#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler

import socketserver
import threading
import argparse
import random
import string
import time
import os


class QuickShare(SimpleHTTPRequestHandler):

    s_uri = ""
    s_filename = ""

    def log_message(self, *args):
        pass

    def do_GET(self):
        s_uri = '/' + self.s_uri
        s_filename = self.s_filename
        s_path = self.path

        if s_path == s_uri:
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200, 'OK')
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(s_filename)))
            self.send_header('Content-Length', os.stat(s_filename).st_size)
            self.end_headers()
            with open(s_filename, 'rb') as b_file:
                self.wfile.write(b_file.read())
        else:
            self.protocol_version = 'HTTP/1.1'
            self.send_response(403, 'Forbidden')
            self.end_headers()

        return


class ThreadedHTTPServer(object):

    server_info = "0.0.0.0:0"

    def __init__(self, host, port, request_handler=QuickShare):
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer((host, port), request_handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

        s_ip, s_port = self.server.server_address
        self.server_info = "{0}:{1}".format(s_ip, s_port)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Quick File Sharing')

    parser.add_argument('-f', action='store', dest='filename',
                        help='file to share')
    parser.add_argument('-u', action='store', dest='uri',
                        default=''.join(random.choice(string.ascii_letters + string.digits) for i in range(10)),
                        help='specify the uri link, default random')
    parser.add_argument('-s', action='store', dest='server',
                        default='0.0.0.0',
                        help='specify the server or ip to listen, default 0.0.0.0')
    parser.add_argument('-p', action='store', dest='port',
                        default='0',
                        help='specify the port to listen, default random')
    parser.add_argument('-t', action='store', dest='time',
                        type=int,
                        default=300,
                        help='specify how long we serve in seconds, default 300s (5 minutes)')

    results = parser.parse_args()

    uri = results.uri
    filename = results.filename
    host = results.server
    port = int(results.port)

    c_length = results.time
    c_start = time.time()

    handler = QuickShare
    handler.s_uri = uri
    handler.s_filename = filename

    server = ThreadedHTTPServer(host, port, request_handler=handler)
    s_info = server.server_info

    print("Starting HTTP Server with URL: http://{0}/{1}".format(s_info, uri))
    server.start()

    try:
        while (True):
            time.sleep(1)
            now = time.time()
            if (now - c_start) > c_length:
                print("Time execution elapsed, closing ...")
                break
    finally:
        server.stop()
