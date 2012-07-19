"""
gevent wsgi server
"""

from gevent import wsgi

import bobo
import sys
import os

sys.dont_write_bytecode = True
rootpath = os.path.dirname(__file__)
dirs = ['', 'disputio']

for d in dirs:
    path = rootpath + d
    if path not in sys.path:
        sys.path.append(path)
        

application = bobo.Application(bobo_resources="disputio.routes")

wsgi.WSGIServer(('', 8088), application, spawn=None).serve_forever()