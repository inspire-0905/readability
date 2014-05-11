import json
import sys
import urllib
import urlparse

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from readability.readability import Document
from urlparse import urlparse, parse_qs

reload(sys)
sys.setdefaultencoding('utf-8')

def parseArticle(url) :

    html = urllib.urlopen(url).read()
    docData = Document(html)
    articleTitle = docData.short_title()
    articleContent = docData.summary()
    return {
        'title': articleTitle,
        'content': articleContent
    }

def handleRequest(self, is_post) :

    reqPath = ''

    if is_post :

        reqPath = self.path

    else :

        parseObj = urlparse(self.path)
        reqPath = parseObj.path

    if reqPath == '/parse' or reqPath == '/parse/' :

        returnData = {
            'result': False,
            'title': 'Request format invalid',
            'content': ''
        }

        try :

            originURL = ''

            if is_post :

                dataLength = self.headers['content-length']
                dataStr = self.rfile.read(int(dataLength))
                jsonData = json.loads(dataStr)
                originURL = jsonData.get('url')

            else :

                queryObj = parse_qs(parseObj.query)
                originURL = queryObj['url'][0]

            articleData = parseArticle(originURL)

            returnData = {
                'result': True,
                'title': articleData['title'],
                'content': articleData['content']
            }

        except Exception, e :

            returnData['content'] = str(e)

        self.send_response(200)
        self.send_header("Content-type:", "application/json")
        self.wfile.write("\n")
        json.dump(returnData, self.wfile)

    else :

        self.send_response(404)
        self.end_headers()

class RequestHandler (BaseHTTPRequestHandler) :

    def do_POST(self) :

        handleRequest(self, True)

    def do_GET(self) :

        handleRequest(self, False)

server = HTTPServer(('0.0.0.0', 80), RequestHandler)

server.serve_forever()