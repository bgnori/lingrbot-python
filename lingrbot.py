#!/usr/bin/env python
#

"""
    for sandboxing read:
        http://developer.plone.org/security/sandboxing.html

    lingr.py is from:
        https://github.com/tsukkee/lingr-vim/blob/master/autoload/lingr.py
"""

from werkzeug import Request, ClosingIterator
from werkzeug.exceptions import HTTPException, InternalServerError

from werkzeug import Response

from werkzeug.routing import Map, Rule


import lingr

import sys

DEBUG = True

url_map = Map([
    Rule("/py27", endpoint="py27"),
    Rule("/", endpoint="index"),
])

def index(request):
    return Response("Hello, world!", mimetype="text/plain")

def py27(request):
    return Response("Python2.7.3!", mimetype="text/plain")

views = {
        'index': index,
        'py27': py27,
        }

class Application(object):
    def __call__(self, environ, start_response):
        try:
            self._setup()
            request = Request(environ)
            if(DEBUG):
                print >> sys.stderr, request.base_url 
                print >> sys.stderr, request.data
            adapter = url_map.bind_to_environ(environ)
            endpoint, values = adapter.match()
            handler = views.get(endpoint)
            response = handler(request, **values)
        except HTTPException, e:
            response = e
        except:
            response = InternalServerError()

        return ClosingIterator(response(environ, start_response), self._cleanup)

    def _setup(self):
        pass
    def _cleanup(self):
        pass

from wsgiref.simple_server import make_server

bot = Application()

from werkzeug import DebuggedApplication

debug = DebuggedApplication(bot)
httpd = make_server('192.168.2.64', 10080, debug)
#httpd = make_server('lingrbot.tonic-water.com', 10080, debug)
httpd.serve_forever()


