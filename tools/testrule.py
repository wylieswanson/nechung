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
    "expire": "2012-03-20 01:42:41"
}'''

print json.dumps( json.loads( rulestr ) )
