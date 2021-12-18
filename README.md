# Youtube to rss
> Don't spend more time than you need to on youtube.com

This is a simple script to generate a .opml file from a list of youtube channels.

Since the subscriptions tab and the little bell that you need to click to **actually** get notifications on new uploads seem to work whenever youtube feels like it *(and since email notifications no longer exist)* I wanted to get an rss feed from the channels I wanted to actually follow. 

Youtube used to have a button to do this but now I can't seem to find a way to follow a channel via RSS. 

## How to get an rss feed for a youtube channel
To get a channels RSS feed:

1. Go to the channel you want to follow
2. Find the channel ID
  - If the url looks like this: `https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw` then the ID is the random string after channelb (ie UCYO_jab_esuFRV4b17AJtAw)
  - If the url has a username like this `https://www.youtube.com/user/USERNAME` you can find their ID by
      * Viewing the page source (Ctrl+U)
      * Search the page (Ctrl+F) for `external_id` or `channel_id` or simply `youtube/channel/` and copy the string that follows.
2. Point to the channel with this url: <br> `https://www.youtube.com/feeds/videos.xml?channel_id=THE_CHANNEL_ID_HERE`

The above is a valid RSS feed you can add to the reader of your choice. You can also follow by user via this link <br> `https://www.youtube.com/feeds/videos.xml?user=USERNAME` and by playlist <br> `https://www.youtube.com/feeds/videos.xml?playlist_id=YOUR_YOUTUBE_PLAYLIST_NUMBER` though there *may* be a querry limit that breaks this, I haven't tested it myself.

## How to get a list of your subscriptions
There also used to be a button to extract your subsciptions to RSS but it is no longer there. The only ways I found to get a list of subscribed channels are: 

1. Crawl this here link [subscription list](https://www.youtube.com/feed/channels) (which is a pain to find as well) and extract the channel links.
2. Do the above by hand
3. Request for an API key and use the [developer console](https://console.developers.google.com/) to possibly get access.
4. Ask for google for your data [here](https://takeout.google.com/). You only need to check the "Youtube and Youtube Music" box. Check in the zip file after downloading for  subscriptions.csv (or similar in case something changes)

Sadly the easiest and least complicated option is number 4. This script will work with any csv that contains channel IDs and names but by default assumes the google takeout format. The choice is given anyway.


## How to use this script
<img align="right" src="./scriptuse.gif">
<p align="left">
  
1. Download the script to a directory you have permissions to write to. (eg Desktop or Downloads should work)
2. Run the script by running the command <br> `python3 youtube-to-rss.py` in your terminal. You need to have [python3 installed](https://realpython.com/installing-python/).
3. Point the script to a .csv file with the youtube channels you want to track via RSS by following the instrucitons.
4. Import the resulting .opml file to the RSS reader of your choice.
  
</p>

<br>

## What does it do ?
This script is mostly user interaction fluff. Basically it looks for a .csv file with a collumn of channel IDs and another of channel names. It then creates the rss links as described above and finally formats them as a basic opml/xml file to import them in a reader. By default it places each channel in its own folder. If this is not the desired behaviour there is a function called `add_channel_nofolder` commmented out in the code. To use that one and have all the channels in a single folder comment out the `add_channel` function, uncommnent the `add_channel_nofolder` and rename it to `add_channel`. (I may add this as a choice in user dialog in the future)
____

<details>
           <summary>Plaintext links just in case</summary>
           <p>
subscription list         - https://www.youtube.com/feed/channels

google takeout            - https://takeout.google.com/

google developer console  - https://console.developers.google.com/

python installation guide - https://realpython.com/installing-python/
             </p>
         </details>
