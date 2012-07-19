# -*- coding: utf-8 -*-

import bobo
import webob
import jinja2
import re

import pymongo as mongo
from bson import objectid
    
    
template_env = jinja2.Environment(loader=jinja2.PackageLoader('disputio', 'templates'))


def get_collection(name = None):
	if name is None:
		name = 'disputio'
	cn = mongo.Connection()
	db = cn.RCE
	col = db[name]
	return col
	

@bobo.query('')
def base(bobo_request):
	return bobo.redirect(bobo_request.url+'/')
	
	
@bobo.query('/')
def root(reponame = None):
	template = template_env.get_template('index.html')
	return template.render({'page':'root'})


	
@bobo.post('/add')
def add(bobo_request):
	doc = {}
	for k in bobo_request.POST:
		doc[k] = bobo_request.POST[k]
	
	col = get_collection()
	col.insert(doc)
	return bobo.redirect('/disputio')
	
	
def r_to_doc(r, keys):
	doc = {}
	for k in keys:
		if k == '_id':
			doc[k] = str(r[k])
		else:
			if r.has_key(k):
				doc[k] = r.get(k)
			else:
				doc[k] = ''
	return doc
	
	
def document_sort_date(a,b):
	da = a.get('_id').generation_time
	db = b.get('_id').generation_time
	if da < db:
		return 1
	elif db < da:
		return -1
	return 0
	
	
@bobo.query('/docs')
def docs():
	col = get_collection()
	res_ = col.find()
	res = []
	for r in res_:
		if len(r.keys()) > 1:
			res.append(r)
		
	res.sort(document_sort_date)
	
	ids = []
	for r in res[0:24]:
		d = {}
		d['id'] = str(r.get('_id'))
		d['time'] = r.get('_id').generation_time.isoformat()
		filt_keys = []
		for k in r.keys():
			if k != '_id':
				filt_keys.append(k)
		d['keys'] = filt_keys
		if r.has_key('title'):
			d['title'] = r['title']
		ids.append(d)
		
	template = template_env.get_template('docs.html')
	return template.render({'ids':ids})


@bobo.query('/value_of')
def value_of(bobo_request):
	key = None
	if 'key' in bobo_request.GET:
		key = bobo_request.GET['key']
		
	if 'key' in bobo_request.POST:
		key = bobo_request.POST['key']	
	
	oid = None
	if 'oid' in bobo_request.GET:
		oid = bobo_request.GET['oid']
		
	if 'oid' in bobo_request.POST:
		oid = bobo_request.POST['oid']	
		
	if key is None:
		return 'Cannot find a key in the request'
	col = get_collection()
	res = col.find({'_id':objectid.ObjectId(oid)})
	if res.count() == 0:
		return ''
	
	doc = res[0]
	if doc.has_key(key):
		return unicode(doc.get(key))
		
	return ''
	
@bobo.query('/:key/:value')
def bykey(key, value):
	col = get_collection()
	pat = {key:value}
	
	if key == 'id' or key == '_id':
		pat = {'_id':objectid.ObjectId(value)}
	
	res = col.find(pat)
	keys_ = {}
	for r in res:
		for k in r.iterkeys():
			keys_[k] = 1
			
	keys = keys_.keys()
	resource = []
	res.rewind()
	for r in res:
		resource.append(r_to_doc(r, keys))
		
	template = template_env.get_template('find.html')
	return template.render({'key':key, 'value':value, 'keys':keys, 'resource':resource})

@bobo.query('/regex/:key/:value')
def byregex(key, value):
	col = get_collection()
	pat = {key:{'$regex':value}}
	
	res = col.find(pat)
	keys_ = {}
	for r in res:
		for k in r.iterkeys():
			keys_[k] = 1
	keys = keys_.keys()
	resource = []
	res.rewind()
	for r in res:
		resource.append(r_to_doc(r, keys))
		
	print('KEYS: %s'%keys)
	print('R: %s'%resource)
		
	template = template_env.get_template('find.html')
	return template.render({'key':key, 'value':value, 'keys':keys, 'resource':resource})


	