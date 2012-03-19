#!/usr/bin/env python

from nechung import nechung

mutator = nechung( 'test' )

def mutation():
	mutator.logger.info( "[+] Service test completed, terminating." )

def main():
	try: mutator.worker( mutation )
	except KeyboardInterrupt: mutator.logger.info( '[*] Service interrupt detected, terminating.' )

if __name__ == "__main__": main()
