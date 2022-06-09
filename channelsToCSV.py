import os, csv, urllib.request
import youtubeToRSS as ytRSS

# Use a given link to lookup channel names by looking for a specific spot in the 
# youtube page.
def crawlForUserName(link,video=False):
	# I'm not using BeautifulSoup because i cant seem to isolate the channel name within
	# tags or anything of the sort. 
	# If anyone can get this to be faster please give it a shot
	if(not video):
		key="\"metadata\":{\"channelMetadataRenderer\":{\"title\":"	
	else:
		key ="\"author\":"	
	with urllib.request.urlopen(link) as response:
   		messOstring = response.read().decode('utf-8')
	target_ind = messOstring.index(key)+len(key)
	char=""
	channel_name=""
	while char!='\"':
		channel_name=channel_name+char
		target_ind+=1
		char=messOstring[target_ind]
	return channel_name

def crawlForChannelID(channelLink):
	key='type=\"application/rss+xml\" title=\"RSS\" href=\"https://www.youtube.com/feeds/videos.xml?channel_id='
	with urllib.request.urlopen(channelLink) as response:
   		messOstring = response.read().decode('utf-8')
	target_ind = messOstring.index(key)+len(key)-1
	char=""
	channelID=""
	while char!='\"':
		channelID=channelID+char
		target_ind+=1
		char=messOstring[target_ind]
	return channelID

def videoLink2channelID(channelName):
	searchLink = 'https://www.youtube.com/results?search_query='+channelName
	key='\"channelRenderer\":{\"channelId\":\"'
	with urllib.request.urlopen(searchLink) as response:
   		messOstring = response.read().decode('utf-8')
	target_ind = messOstring.index(key)+len(key)-1
	char=""
	channelID=""
	while char!='\"':
		channelID=channelID+char
		target_ind+=1
		char=messOstring[target_ind]
	return channelID

def run():
	#Initializing script variables
	loop   = True
	create = False
	header =['Channel-ID','blank','Channel-Name']

	# Some lists to check user input
	yes = ["Y","y","YES","yes",""] #empty string to use as default when pressing enter.
	no  = ["N","n","NO","no"]
	quit =["Q","q"]
	# Script main loop
	while loop:
		print("Create new youtube channel csv? [Y/n] ")
		try:
			create_new = input("")
		except Exception as e:
			ytRSS.printRed("Unexpected error.")
			print(e)
			ytRSS.printRed("exiting")
			exit()
		else:
			if create_new in quit:
				exit()
			elif create_new not in (yes+no):
				ytRSS.printRed("Please enter y/n.")
			elif create_new in yes:
				create = True
				loop=False
			else:
				loop=False
	loop=True

	csvfilename="ytchannelsToFollow.csv"
	count=0
	if create:
		while loop:
			try:
				csvfile=open(csvfilename,"x")
				loop=False
			except FileExistsError as fileExists:
				count+=1
				csvfilename="ytchannelsToFollow_"+str(count)+".csv"	
			except Exception as e:
				ytRSS.printRed("Unexpected Error!")
				print(e)
				ytRSS.printRed("exiting")
				exit()
	csvwriter = csv.writer(csvfile, delimiter=",", quotechar='"')
	csvwriter.writerow(header)
	
	loop=True
	buntchOfLinksFile=False
	while loop:
		print("Add channels from file? [Y/n] \n Should be one link per row of a channel/user or video.")
		try:
			create_new = input("")
		except Exception as e:
			ytRSS.printRed("Unexpected error.")
			print(e)
			ytRSS.printRed("exiting")
			exit()
		else:
			if create_new in quit:
				exit()
			elif create_new not in (yes+no):
				ytRSS.printRed("Please enter y/n.")
			elif create_new in yes:
				buntchOfLinksFile = True
				loop=False
			else:
				loop=False
	loop=True

	if(buntchOfLinksFile):
		while loop:
		    print("Enter youtube link list filename. If the file is in a different directory press q.")
		    # Limiting imput to current director to handle errors.
		    # Also assuming no familiarity with python or scripts and where they run etc.
		    # Or thats what I intend anyway
		    buntchOfLinks = os.path.dirname(os.path.abspath(__file__)) +"/"+ input( os.path.dirname(os.path.abspath(__file__))+"/")
		    if buntchOfLinks==os.path.dirname(os.path.abspath(__file__)) +"/"+ "q" :
		      print("Enter full path to subscription csv. q to exit")
		      buntchOfLinks = input("")
		    if(buntchOfLinks=="q"):
		      exit()
		    try:
		      linkFile = open(buntchOfLinks, mode ='r')
		    except FileNotFoundError as fileNotFound:
		      printRed("Invalid file name.")
		    except Exception as e:
		      printRed(e)
		    else:
		      loop=False

	loop=True
	video=False
	channelLink=""
	channelID=""
	skip=False

	while loop:
		 try:
		 	if(not buntchOfLinksFile):
		 		channel= input("Enter youtube link. [Enter to stop adding.]\n")
		 	else:
		 		channel=linkFile.readline()
		 		if not channel:
		 			print('End of File!')
		 			linkFile.close()
		 			csvfile.close()
		 			exit()

		 except Exception as e:
		 	ytRSS.printRed("Unexpected Error!")
		 	print(e)
		 	ytRSS.printRed("exiting")
		 	exit()
		 else:
		 	skip=False
		 	if(channel==""): 
		 		loop=False
		 		csvfile.close()
		 		skip=True
		 	channel_split=channel.split("/")
		 	
		 	if channel_split[len(channel_split)-2] == "channel":
		 		print("Detected as channel link")
		 		channelID = crawlForChannelID(channel)
		 		channelName = ytRSS.check_reserved(crawlForUserName(channel))
		 	elif channel_split[len(channel_split)-2] == "c" or channel_split[len(channel_split)-2] == "user" :
		 		print("Detected as user link")
		 		channelID = crawlForChannelID(channel)
		 		channelName = ytRSS.check_reserved(crawlForUserName(channel))
		 	elif "watch" in channel_split[len(channel_split)-1]:
		 		print("Detected as video link")
		 		video=True
		 		channelName = ytRSS.check_reserved(crawlForUserName(channel,video))
		 		channelID = videoLink2channelID(channelName.replace(" ", ""))
		 	elif channel!="":
		 		ytRSS.printRed("Unable to parse link.\n" )
		 		print("Please enter youtube channel link or youtube video link.")
		 		skip=True
		 	
		 	if(not skip):
		 		csvwriter.writerow([channelID,"",channelName] )
		 		print("Added "+ channelName+" and ID: "+channelID+" to "+csvfilename)


if __name__== "__main__":
	run()
	print("ytchannelsToFollow")