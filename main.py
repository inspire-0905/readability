import json
import sys
import urllib

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from readability.readability import Document

reload(sys)
sys.setdefaultencoding('utf-8')

def parseArticle(url):

    html = urllib.urlopen(url).read()
    docData = Document(html)
    articleTitle = docData.short_title()
    articleContent = docData.summary()
    return {
        'title': articleTitle,
        'content': articleContent
    }

class RequestHandler (BaseHTTPRequestHandler) :

    def do_POST(self) :

        if self.path == "/parse" :

            returnData = {
                'result': False,
                'title': 'Parse URL Article Failed',
                'content': ''
            }

            try:

                dataLength = self.headers['content-length']
                dataStr = self.rfile.read(int(dataLength))
                jsonData = json.loads(dataStr)
                originURL = jsonData.get('url')
                articleData = parseArticle(originURL)

                returnData = {
                    'result': True,
                    'title': articleData['title'],
                    'content': articleData['content']
                }

            except Exception, e:

                returnData['content'] = str(e)

            self.send_response(200)
            self.send_header("Content-type:", "application/json")
            self.wfile.write("\n")
            json.dump(returnData, self.wfile)

        else:

            self.send_response(200)
            self.end_headers()

server = HTTPServer(('0.0.0.0', 80), RequestHandler)

server.serve_forever()