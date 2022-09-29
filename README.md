# Youtube to rss

Scripts to help add a youtube subscription feed to an RSS reader.

Since the subscriptions tab and the little bell that you need to click to **actually** get notifications on new uploads seem to work whenever youtube feels like it *(and since email notifications no longer exist)* I wanted to get an rss feed from the channels I wanted to actually follow. 

Youtube used to have a button to do this but now I can't seem to find a way to follow a channel via RSS. 

## tl;dr 

1. `git clone https://github.com/Kostas-F/youtube-to-rss`
2. `cd ./youtube-to-rss`
    - If creating a channel list csv: `pip install -r requirements.txt` and `python3 channelsToCSV.py`
3. `python3 youtubeToRSS.py`

## How to get an rss feed for a youtube channel
To get a channels RSS feed:

1. Go to the channel you want to follow
2. Find the channel ID
  - If the url looks like this: `https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw` then the ID is the random string after channelb (ie `UCYO_jab_esuFRV4b17AJtAw`)
  - If the url has a username like this `https://www.youtube.com/user/USERNAME` you can find their ID by
      * Viewing the page source (Ctrl+U)
      * Search the page (Ctrl+F) for `external_id` or `channel_id` or simply `youtube/channel/` and copy the string that follows.
3. The channel feed is this url : <br> `https://www.youtube.com/feeds/videos.xml?channel_id=THE_CHANNEL_ID_HERE`

The above is a valid RSS feed you can add to the reader of your choice. You can also follow by user via this link <br> `https://www.youtube.com/feeds/videos.xml?user=USERNAME` and by playlist <br> `https://www.youtube.com/feeds/videos.xml?playlist_id=YOUR_YOUTUBE_PLAYLIST_NUMBER` though there *may* be a querry limit that breaks this, I haven't tested it myself.

## How to get a list of your subscriptions
There also used to be a button to extract your subsciptions to RSS but it is no longer there. The possible ways I found to get a list of your subscribed channels are: 

1. Crawl your [subscription list](https://www.youtube.com/feed/channels) (which is a pain to find as well) and extract the channel links.
2. Do the above by hand
3. Request for an API key and use the [developer console](https://console.developers.google.com/) to possibly get access. Personally I have no experience with this.
4. Ask for google for your data [here](https://takeout.google.com/). You only need to check the "Youtube and Youtube Music" box. Check in the zip file after downloading for  subscriptions.csv (or similar in case something changes)
5. Use the channelsToCSV script in this repo to get channel IDs and names. See [this section for more detailed instuctions](#how-to-use-channelID-extraction-script)

This script will (hopefully) work with any csv that contains channel IDs and names.

## How to use this script
<img align="right" src="./scriptuse.gif" title="Best case scenario">
<p align="left">
  
1. Download the script to a directory you have permissions to write to. (eg Desktop or Downloads should work)
2. Run the script by running the command <br> `python3 youtubeToRSS.py` in your terminal. You need to have [python3 installed](https://realpython.com/installing-python/).
3. Point the script to a .csv file with the youtube channels you want to track via RSS by following the instrucitons.
4. Import the resulting .opml file to the RSS reader of your choice.

(The gif uses an old scipt name.)

</p>

<br>

## How to use channelID extraction script

1. Download _both_ scripts in a directory you have permissions to write to.
2. To run the script you need to have [python3 installed](https://realpython.com/installing-python/). Also you need to run `pip install -r requirements.txt` in the directory you downloaded the scripts to install any missing modules you may not have installed (at this point this installs only urlib3)
3. Run the script by running the command `python3 channelsToCSV.py` in your terminal.
4. Point the script to a textfile with links in each line. Links can point to channels or individual videos. You can also add them one by one.
5. Use the resulting .csv file with `youtubeToRSS.py`.

<details>
           <summary>Plaintext links</summary>
           <p>
subscription list         - https://www.youtube.com/feed/channels

google takeout            - https://takeout.google.com/

google developer console  - https://console.developers.google.com/

python installation guide - https://realpython.com/installing-python/
             </p>
         </details>
