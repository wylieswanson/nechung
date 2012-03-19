#!/usr/bin/env python

import pika, logging, json, ConfigParser
from optparse import OptionParser

class nechung:

	def	__init__(self, mutator):
		self.mutator = mutator

		self.parser = OptionParser( usage= "usage: %prog [options]", version="%prog 1.0")
		self.parser.add_option("-c", "--config", dest="config", help="use alternate account configuration")
		self.parser.add_option("-w", "--worker", dest="worker", help="identify worker number for troubleshooting")
		(options, args) = self.parser.parse_args()
		
		if options.worker: worker=options.worker
		else: worker=str(0)

		self.cfg = ConfigParser.ConfigParser()
		self.cfg.read( "/etc/agile/nechung/nechung.conf" )

		self.queue=self.cfg.get( "MutatorQueues", self.mutator )
		self.log=self.cfg.get( "MutatorLogs", self.mutator )
		self.host=self.cfg.get('MQ','host')
		self.user=self.cfg.get("MQ",'user')
		self.password=self.cfg.get("MQ",'password')

		self.logger = logging.getLogger(self.mutator)
		self.hdlr = logging.FileHandler(self.log)
		self.formatter = logging.Formatter('%(asctime)s nechung.'+self.mutator+'('+worker+') %(message)s')
		self.hdlr.setFormatter(self.formatter)
		self.logger.addHandler(self.hdlr)
		self.logger.setLevel(logging.INFO)

	def callback(self, ch, method, properties, body):
		self.payload = json.loads(body)
		self.mutation()
		ch.basic_ack(delivery_tag = method.delivery_tag)

	def worker(self,mutation):
		self.mutation=mutation
		connection = pika.BlockingConnection(pika.ConnectionParameters( host=self.host, credentials=pika.PlainCredentials( self.user, self.password ) ) )
		channel = connection.channel()
		channel.queue_declare(queue=self.queue, durable=True)
		self.logger.info('[*] Waiting for messages. Use \'sv\' to manage service.')
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(self.callback, queue=self.queue) 
		channel.start_consuming()


