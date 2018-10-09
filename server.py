#!/usr/bin/env python3

'''

 Copyright 2018 Sebastian Glahn

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

'''

import os
import argparse
import hashlib
import glob
import logging
import ssl
import http.server

FIRMWARE_DIRECTORY = os.environ['HOME'] + os.sep + "firmware"

class HttpHandler(http.server.BaseHTTPRequestHandler):

    def getLatestFirmwareVersion(self, flavor):
        for firmware in os.listdir(FIRMWARE_DIRECTORY):
            if firmware.startswith(flavor):
                return firmware[firmware.index("-") +1:firmware.index('.bin')]
        return -1     

    def validRequest(self, flavor):
        return glob.glob(FIRMWARE_DIRECTORY + os.sep + flavor + '*') and 'x-ESP8266-version' in self.headers

    def buildHtmlResponse(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
       
    def buildStreamResponse(self, flavor, latest):
        filename = FIRMWARE_DIRECTORY + os.sep + flavor + '-' + latest + ".bin"
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('Content-Disposition', 'attachment; filename=' + filename)
        self.send_header('Content-Length', os.path.getsize(filename))
        self.send_header('x-MD5', hashlib.md5(open(filename, 'rb').read()).hexdigest())
        self.end_headers()
        with open(filename, 'rb') as binary:
            self.wfile.write(binary.read())

    def do_GET(self):
        log_stat = { 'ip' : self.client_address[0] }
        flavor = self.path.rsplit('/', 1)[-1]

        if not self.validRequest(flavor):
            logging.error('Invalid request', extra = log_stat)
            self.buildHtmlResponse(400)
            return
        
        latest = self.getLatestFirmwareVersion(flavor)
        firmware_version = self.headers.get('x-ESP8266-version')
        if float(latest) > float(firmware_version):
            logging.info('Sending firmware update for ' + flavor + ' from ' + firmware_version + ' to ' + latest + '.', extra = log_stat)
            self.buildStreamResponse(flavor, latest)
            return
        else:
            logging.debug('No update available', extra = log_stat)
            self.buildHtmlResponse(304)
            return


def parseArgs():
    parser = argparse.ArgumentParser(description='HTTP Server which delivers firmware binaries for Arduino OTA updates.')
    parser.add_argument('--dir', help='Directory containing the firmware binaries to serve. Default: ~/firmware', default=os.environ['HOME'] + os.sep + "firmware")
    parser.add_argument('--port', help='Server port. Default: 8000.', default=8000)
    parser.add_argument('--log', help='Log level. Default ERROR', default='INFO')
    parser.add_argument('--cert', help='SSL cert file to enable HTTPS. Default empty=No HTTPS', default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArgs()

    if args.dir:
        FIRMWARE_DIRECTORY = args.dir

    logging.basicConfig(format='%(asctime)-15s %(levelname)s %(ip)s --- %(message)s', level=args.log)

    try:
        server = http.server.HTTPServer(('', args.port), HttpHandler)
        if args.cert:
            server.socket = ssl.wrap_socket(server.socket, certfile=args.cert, server_side=True)

        print('Started httpserver on port ' + str(args.port) + ', firmware directory: ' + FIRMWARE_DIRECTORY)
        server.serve_forever()

    except KeyboardInterrupt:
        print('Shutting down httpserver')
        server.socket.close()
