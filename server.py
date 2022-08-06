#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os

def get_config_map():
    mapping = {}
    with open(os.path.join(os.getcwd(), 'mapping.cfg'), 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith('#'):
                continue
            line = line.strip()
            if len(line) == 0:
                continue
            request_path = line;
            line = f.readline()
            if not line:
                break
            response_file_path = line.strip()
            mapping[request_path] = response_file_path
    return mapping



class FileHandler(BaseHTTPRequestHandler):
    def __init__(self, config_map, *args, **kwargs):
        logging.info('init...\n')
        self.request_path_to_relative_path = config_map
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def _set_status(self, status_code):
        self.send_response(status_code)
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        file_relative_path = self.request_path_to_relative_path.get(self.path)
        if (file_relative_path == None):
            self._set_status(404)
        else:
            self._set_status(200)
            with open(os.path.join(os.getcwd(), 'data', file_relative_path), 'rb') as f:
                chunk_size = 1024
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    self.wfile.write(data)

def run(server_class=HTTPServer, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    def handler(*args):
        FileHandler(get_config_map(), *args)
    httpd = server_class(server_address, handler)
    logging.info('Starting httpd... [port={}]\n'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
