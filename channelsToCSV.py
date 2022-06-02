import os,csv,urllib.request
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

def run():
	#Initializing script variables
	loop   = True
	create = False

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
	loop=True
	video=False
	while loop:
		 try:
		 	channel= input("Enter youtube link. [Enter to stop adding.]\n")
		 except Exception as e:
		 	ytRSS.printRed("Unexpected Error!")
		 	print(e)
		 	ytRSS.printRed("exiting")
		 	exit()
		 else:
		 	if(channel==""): loop=False
		 	channel_split=channel.split("/")
		 	if channel_split[len(channel_split)-2] == "channel":
		 		print("Detected as channel link")
		 		channelName = crawlForUserName(channel)
		 	elif channel_split[len(channel_split)-2] == "c" or channel_split[len(channel_split)-2] == "user" :
		 		print("Detected as user link")
		 		channelName = crawlForUserName(channel)
		 	elif "watch" in channel_split[len(channel_split)-1]:
		 		print("Detected as video link")
		 		video=True
		 		channelName = crawlForUserName(channel,video)
		 	print("Added "+ channelName+" to "+csvfilename)

if __name__== "__main__":
	run()