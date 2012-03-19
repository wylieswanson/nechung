#!/usr/bin/env python
import json, os, shutil, subprocess, tempfile, time, sys
from datetime import datetime
from AgileCLU import AgileCLU

recording = "Billy the Exterminator Roadkill"
recording = "Big Buck Bunny"
recording = "Frozen Planet The Ends of the Earth"

rulestr = '''{ 
    "condition": {
        "exist": [ "/Transcode/Video3/iOS/'''+recording+'''.appletv2.m4v", "/Transcode/Video3/iOS/'''+recording+'''.iphone.m4v", "/Transcode/Video3/iOS/'''+recording+'''.high.m4v" ]
    },
    "action": {
        "writetextfile": [
				{
	            "body": "/Transcode/Video3/iOS/'''+recording+'''",
					"object": "/TV/make.iphonetv.embed.html"
				},
				{
					"body": "/Transcode/Video3/iOS/'''+recording+'''.high.m4v",
					"object": "/TV/make.video.embed.html"
				}
        ]
    },
    "expire": "2012-03-20 00:15:00"
}'''

OK = 0

def actions():
	global OK
	if 'action' in rule and not (rule['action'] is None):
		print "[+] There is an action specified"
		if 'writetextfile' in rule['action'] and not (rule['action']['writetextfile'] is None):

			print "[+] Executing writetextfile action"

			tempdir = tempfile.mkdtemp( 'nechung-rules' )
			for textfile in rule['action']['writetextfile']:
				f = open( tempdir+'/'+os.path.basename(textfile['object']), "w")
				print "[?] FILE "+os.path.basename(textfile['object']) 
				print "[?] BODY "+textfile['body'] 
				f.write( textfile['body'] )
				f.close()
				subprocess.call( ['/usr/local/bin/agilepost', '-l', 'wylie', tempdir+'/'+os.path.basename(textfile['object']), os.path.dirname(textfile['object']) ] )

			shutil.rmtree(tempdir)
		else:
			print "[-] We are not building any text instructions"
	else:
		print "[-] No action has been specified"

def conditions():
	global OK
	if 'condition' in rule and not (rule['condition'] is None):
		print "[+] There is a condition"
		if 'exist' in rule['condition'] and not (rule['condition']['exist'] is None):

			print "[+] Objects must exist"
			while (OK<>len(rule['condition']['exist'])):
				for object in rule['condition']['exist']:
					if agile.fexists(object): 			
						OK += 1 ; print "[+] OK "+object
					else:										
						OK -= 1 ; print "[-] NOT OK "+object
				if (OK==len(rule['condition']['exist'])):
					print "[+] The objects are ready!"
				else:
					print "[-] The "+str(len(rule['condition']['exist']))+" objects are NOT ready. Retrying in 10 minutes..."
					OK = 0 ; time.sleep(600)
	
		else:
			print "[-] We don't care about objects"
	else: 
		print "[-] There is not condition"
	return OK




def main():
	global rule, agile

	rule = json.loads(rulestr)

	expire = time.strptime( rule['expire'], '%Y-%m-%d %H:%M:%S' )
	now = time.localtime()

	if now > expire:
		print "[!] Rule has expired"
	else:

		agile = AgileCLU('wylie')
		try: 
			OK = conditions()
			if (OK>0): actions()
		except KeyboardInterrupt: 
			print '[*] Service interrupt detected, terminating.' 
		agile.logout()

if __name__ == "__main__": main()
