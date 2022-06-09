import os,csv

# Use ANSI to print red text for errors
def printRed(text): print("\033[91m {}\033[00m".format(text))

# Checking for xml reserved characters
def check_reserved(name):
  # It is important to check for ampersand first
  xml_reserves=['&','<','>','\'','\"']
  xml_entites =["&amp;","&lt;","&gt;","&apos;","&quot;"]
  index = 0
  ind_replace=[]
  for ch in xml_reserves:
    # Traversing sting and saving index of reserved char to list
    # in order to catch possible multiple uses of reserved char in
    # the string
    while index < len(name):
      index = name.find(ch, index)
      if index == -1:
        break
      ind_replace.append(index)
      index+=1
    # Reversing the string to replace from end to start, in order to
    # use the previously indexed locations without adding the length 
    # of the enties each time and for each type.  
    ind_replace.reverse()
    for ind_r in ind_replace:
      name = name[0:ind_r]+xml_entites[xml_reserves.index(ch)]+name[ind_r+1:]
    # Reset to keep checking for the other reserves
    ind_replace=[]
    index=0
  return name

# Starting a simple opml file with a folder
def preamble(file):
  file.write("<opml version=\"2.0\">\n<body>\n<outline text=\"Youtube Subscriptions\" title=\"Youtube Subscriptions\">\n") 

# Adding a youtube channel feed with its own subfolder
def add_channel(chanel_name,file,channel_ids,channel_names):
  file.write("<outline title=\""+chanel_name+"\">\n")
  file.write("<outline type=\"rss\" xmlUrl='https://www.youtube.com/feeds/videos.xml?channel_id="+channel_ids[channel_names.index(chanel_name)]+"'/>\n")
  file.write("</outline>\n")  

# Adding a youtube channel feed without a folder
# def add_channel_nofolder(chanel_name,file):
#   file.write("<outline type=\"rss\" xmlUrl='https://www.youtube.com/feeds/videos.xml?channel_id="+channel_ids[channel_names.index(chanel_name)]+"'/>\n")

# Ending the opml file
def afterword(file):
  file.write("</outline>\n</body>\n</opml>")

def run():
  # Initializing script variables
  channel_ids   = []
  channel_names = []
  loop          = True
  # Default filename to create. Used in user dialog.
  opmlfilename="youtube-subscriptions.opml"
  # Some lists to check user input
  yes = ["Y","y","YES","yes",""] #empty string to use as default when pressing enter.
  no  = ["N","n","NO","no"]

  # Script default values for navigating file, *assuming file from google takeout*.
  default    = True
  adding     = False
  header     = True
  ID_index   = 0
  NAME_index = 2
  ## Script start
  # The loops serve to limit errors and get usable input from the user.
  while loop:
    print("Enter csv filename. If the file is in a different directory press q.")
    # Limiting imput to current director to handle errors.
    # Also assuming no familiarity with python or scripts and where they run etc.
    # Or thats what I intend anyway
    subs_csv = os.path.dirname(os.path.abspath(__file__)) +"/"+ input( os.path.dirname(os.path.abspath(__file__))+"/")
    if subs_csv==os.path.dirname(os.path.abspath(__file__)) +"/"+ "q" :
      print("Enter full path to subscription csv. q to exit")
      subs_csv = input("")
    if(subs_csv=="q"):
      exit()
    try:
      file = open(subs_csv, mode ='r')
    except FileNotFoundError as fileNotFound:
      printRed("Invalid file name.")
    except Exception as e:
      printRed(e)
    else:
      loop=False

  print("Are you using the .csv from a google takeout? ([Y]/n)")
  loop=True
  while loop:
    try:
      dftl_chk = input("")
    except Exception as e:
      printRed(e)
    else:
      if(dftl_chk in no):
        default=False
        loop=False
      elif(dftl_chk in yes):
        print("Assuming the file has a header, channel ids are in collumn 0 and names in collumn 2.")
        loop=False
      else:
        printRed("Please enter Y or n.")  
    
  if(not default):
    print("Does the csv have a header (ie. Does the fist row have title of collumns)? ([Y]/n)")
    loop=True
    while loop:
      try:
        header_chk=input("")
      except Exception as e:
        print(e)
      else:
        if(header_chk in no):
          header=False
          loop=False
          print("Handling csv as if no header exits.")
        elif(header_chk in yes):
          loop=False
          print("Handling csv as if it has a header.")
        else:
          printRed("Please enter Y or n")

    loop=True
    while loop:
      print("Which collumn in the .csv file contains channel ids?")
      ID_index=input("")
      try:
        ID_index=int(ID_index)
      except ValueError as notNumeric:
        printRed("Please enter a number (integer)")
      except Exception as e:
        printRed(e)
      else:
        print("Looking for channel ids in collumn number"+str(ID_index))
        loop=False
      
    loop=True
    while loop:
      print("Which collumn in the .csv file contains channel names?")
      NAME_index=input("")
      try:
        NAME_index=int(NAME_index)
      except ValueError as notNumeric:
        printRed("Please enter a number (integer)")
      except Exception as e:
        printRed(e)
      else:
        print("Looking for channel names in collumn number"+str(NAME_index))
        loop=False

  # Harvesting data from the csv file
  csvFile = csv.reader(file)
  if header:
    next(csvFile)
  for line in csvFile:
    channel_ids.append(line[ID_index])
    channel_names.append(check_reserved(line[NAME_index]))
  file.close()
  
  # Creating or adding to the opml file.
  loop=True
  innerloop=True
  count=0
  # this loop is used to generate a valid file name if the name is already in use
  while loop:
    try:
      if(count>=1): 
        rssfile = open("youtube-subscriptions_"+str(count)+".opml","x") 
        loop=False
        opmlfilename="youtube-subscriptions_"+str(count)+".opml"
      else:
        rssfile = open("youtube-subscriptions.opml","x") 
        loop=False    
    except FileExistsError as fileExists:
      if(count==0):
        print("Found an oplml file (youtube-subscriptions.opml) possibly created previously.\nDo you want to attempt to add subscriptions (A) or create a new file [C] ?\nAdding to a file not created by this script will probably mess that file up.")
        # loop to get desired input
        while innerloop:
          try:
            choice=input("")
          except Exception as e:
            printRed(e)
          else:
            if(choice=="A"):
              # Exit out of both this and the outer loop and go try adding channels to an existing file
              loop=False
              adding=True
              innerloop=False
            elif(choice=="C"):
              # Exit out of inner loop and loop until a valid name is achieved
              innerloop=False
            else:
              # Loop again in the inner to validate input
              printRed("Please enter A or C")
      count+=1
    except Exception as e:
      printRed(e)
      print("Unexpected error. Exiting.")
      exit()
      

  if(not adding):
    # Create a new file from the csv data
    preamble(rssfile)
    for channel in channel_names:
      add_channel(channel,rssfile,channel_ids,channel_names)
    afterword(rssfile)
    rssfile.close()
    print("Created a .opml file from the channels in the .csv \n"+os.path.dirname(os.path.abspath(__file__))+"/"+opmlfilename+"\nYou can now add the channels to an rss reader.")
  else:
    # Trying to add to an existing opml file. 
    try:
      rssfile = open("youtube-subscriptions.opml","r") 
    except Exception as e:
      printRed("Error while trying to read existing .opml file.\n")
      printRed(e)
      exit()
    oldrss=rssfile.readlines()
    rssfile.close()
    with open("youtube-subscriptions.opml.tmp","x") as newrssfile:
      linenum= oldrss.index("</body>\n")
      for i in range(0,linenum-1):
        newrssfile.write(oldrss[i])
      for channel in channel_names:
        add_channel(channel,newrssfile,channel_ids,channel_names)
      afterword(newrssfile)
    os.remove("youtube-subscriptions.opml")
    os.rename("youtube-subscriptions.opml.tmp", "youtube-subscriptions.opml")
    print("Attempted to add the channels to youtube-subscriptions.opml")

if __name__== "__main__":
  run()