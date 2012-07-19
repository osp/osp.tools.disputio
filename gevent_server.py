"""
gevent wsgi server
"""

import sys
import os
import argparse

import bobo

from gevent import wsgi


sys.dont_write_bytecode = True
rootpath = os.path.dirname(__file__)
dirs = ['', 'disputio']

for d in dirs:
    path = rootpath + d
    if path not in sys.path:
        sys.path.append(path)
        
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', "--address", help="Address to bind to", default='')
	parser.add_argument('-p', "--port", help="Port to listen to", default=8000, type=int)
	parser.add_argument('-l', "--log", help="gevent logging", default=None)
	args = parser.parse_args()
	
	app = bobo.Application(bobo_resources="disputio.routes")
	wsgi.WSGIServer((args.address, args.port), application=app, spawn=None, log=args.log).serve_forever()
	
	
if __name__ == '__main__':
	main()