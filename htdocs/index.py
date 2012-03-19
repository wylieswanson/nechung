#!/usr/bin/env python
from mod_python import util
import re
import urllib, os.path, sys
import datetime, dateutil.relativedelta, time
import ConfigParser
import logging
import pika
import json

cfg = ConfigParser.ConfigParser()
cfg.read( "/etc/agile/nechung/nechung.conf" )

htreceiver_queue = cfg.get( "Queues", "htreceiver_queue" )
htreceiver_log = cfg.get( "Nechung", "htreceiver_log" )
mt = cfg.get( "Agile", "mt" )
fsroot = cfg.get( "Agile", "fsroot" )

logger = logging.getLogger( 'nechung-htreceiver' )
hdlr = logging.FileHandler( htreceiver_log )
formatter = logging.Formatter( '%(asctime)s nechung-htreceiver %(message)s' )
hdlr.setFormatter( formatter ) ; logger.addHandler( hdlr ) ; logger.setLevel( logging.INFO )

uuid = str( None ) ; path = str( None ) ; object_url = str( None ) ; object_path = str( None ) ; object_name = str( None ) ; object_prefix = str( None ) ; object_ext = str( None ) ; size = str( None ) ; uid = str( None ) ; gid = str( None ) ; ctime = str( None ) ; mtime = str( None ) ; callbacktime = str( None ) ; object_write_path = str( None )
action = str( None )

def parse_request( req ):
	global action, uuid, path, size, uid,gid, ctime, mtime, callbacktime, object_url, object_name, object_path, object_write_path, object_prefix, object_ext
	form = util.FieldStorage( req, keep_blank_values=1 )
	if form.has_key( "p" ): 
		path = str( form.getfirst( "p" ) ) ; object_url = mt + path  ; path = urllib.unquote( path )
 		object_name = os.path.basename( path ) ; object_path = os.path.dirname( path ) ; object_write_path = object_path.replace( fsroot, "" )
		object_array = os.path.splitext( object_name ) ; object_prefix = object_array[0] ; object_ext = object_array[1]
	if form.has_key( "a" ): action = str( form.getfirst( "a" ) )  			
	if form.has_key( "u" ): uuid = str( form.getfirst( "u" ) )  			
	if form.has_key( "s" ): size = str( form.getfirst( "s" ) )  			
	if form.has_key( "U" ): uid = str( form.getfirst( "U" ) )  			 	
	if form.has_key( "G" ): gid = str( form.getfirst( "G" ) )  			 	
	if form.has_key( "c" ): ctime = str( form.getfirst( "c" ) ) 			
	if form.has_key( "m" ): mtime = str( form.getfirst( "m" ) ) 			
	if form.has_key( "T" ): callbacktime = str( form.getfirst( "T" ) )	
	# logger.info( "[@] uuid=" + uuid + ", path=" + path + ", size=" + size + ", owner=" + uid + "/" + gid + ", time=" + ctime + "/" + mtime + "/" + callbacktime )

def queue_request():
	connection = pika.BlockingConnection( pika.ConnectionParameters( host=cfg.get('MQ','host'), credentials=pika.PlainCredentials( cfg.get('MQ','user'), cfg.get('MQ','password') ) ) )
	channel = connection.channel()
	channel.queue_declare(queue=htreceiver_queue, durable=True)

	message='{ "action": "' + action + '", "url": "' + object_url + '", "path": "' + path + '", "object": { "path": "' + object_path + '", "write_path": "' + object_write_path + '", "name": "' + object_name + '", "prefix": "' + object_prefix + '", "ext": "' + object_ext + '"}, "stat": { "size": ' + size + ', "uuid": "' + uuid + '", "uid": ' + uid + ', "gid": ' + gid + ', "ctime": ' + ctime + ', "mtime": ' + mtime + ' }, "cbtime": ' + callbacktime + ' }'

	channel.basic_publish(exchange='', routing_key=htreceiver_queue, body=message, properties=pika.BasicProperties( delivery_mode = 2))
	connection.close()
	logger.info( "[+] " + action + " - " + path )


def index( req ):
	req.content_type = 'text/html' ; msg = "" ; timestamp = time.strftime( '%Y-%m-%d %H:%M:%S' )
	parse_request( req ) ; queue_request() ; return msg

if __name__ == '__main__':
	index( html )

