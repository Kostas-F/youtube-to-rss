import os,csv
from ./youtube-to-rss.py import printRed
loop       = True
create = False
# Script main loop
while loop:
	printRed("Create new youtube channel csv?")
	try:
		creat_new = input("")
	except Exception as e:
		printRed(e)
	else:
		pass
	finally:
	 	pass 
