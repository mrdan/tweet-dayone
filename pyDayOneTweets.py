#!/usr/bin/python

import json, urllib, urllib2, subprocess, re, sys, time, os
from datetime import datetime, timedelta

# Script settings
lastid_filename = "pydayone_lastid.txt"

# Twitter settings
twitter_username = "mrdan"  # guess
tweet_count = 200           # How many tweets to pull down at a time, the higher the number the less frequently you should run the script
retweets = 1                # 1 to include retweets and 0 to exclude them. Retweets are included in the tweet_count no matter what you pick here
tweet_photos = 1            # 1 to include photos in the tweet

try:
    lastid_file = open(lastid_filename, 'r')
    lastid = int(lastid_file.readline())
    lastid_file.close()
except:
    lastid = 0

new_lastid = lastid

request_string = 'https://api.twitter.com/1/statuses/user_timeline.json?screen_name=' + twitter_username + '&count=' + str(tweet_count) + '&include_rts=' + str(retweets) + '&include_entities=' + str(tweet_photos)
if lastid > 0:
    request_string = request_string + '&since_id=' + str(lastid)
try:
    request = urllib2.Request(request_string)
    response = urllib2.urlopen(request)
    data = response.read()
    tweets = json.loads(data, encoding='utf_8')
except:
    sys.exit()

for tweet in tweets:
    image_file_name = ''

    if int(tweet['id']) > lastid:
        tweet_text = "@" + twitter_username + ":  " + tweet['text']

        tweet_time = tweet['created_at']
        tweet_time = re.sub(r'\+[0-9]+ ', '', tweet_time) # strip out the timezone info
        our_date = datetime.strptime(tweet_time, "%a %b %d %H:%M:%S %Y")
        tz_diff = int(tweet['user']['utc_offset'])
        our_date = our_date + timedelta(seconds=tz_diff) # apply user profile timezone info
        our_date = our_date.strftime("%Y-%m-%d %H:%M:%S")

        if tweet['in_reply_to_status_id']:
            req_their_tweet = urllib2.Request('https://api.twitter.com/1/statuses/show.json?id=' + str(tweet['in_reply_to_status_id']))
            try:
                res_their_tweet = urllib2.urlopen(req_their_tweet)
                data_their_tweet = res_their_tweet.read()
                their_tweet = json.loads(data_their_tweet, encoding='utf_8')
                tweet_text = tweet_text + '   (in reply to: "' + their_tweet['text'] + '")'
            except:
                pass

        try:
            if tweet['entities']['media'][0]['type'] == 'photo':
                img_url = tweet['entities']['media'][0]['media_url_https']
                image_file_name = re.search('[a-z,A-Z,0-9]+(.(jpg|png|gif))', img_url, re.IGNORECASE)
                image_file_name = image_file_name.group(0)
                image = urllib.URLopener()
                image.retrieve(img_url, image_file_name)
        except:
            pass

        echo = subprocess.Popen(['echo', tweet_text], stdout=subprocess.PIPE)
        if image_file_name == '':
            dayone = subprocess.Popen(['dayone', '--date="'+our_date+'"', 'new'], stdin=echo.stdout, stdout=subprocess.PIPE)
        else:
            dayone = subprocess.Popen(['dayone', '--date="'+our_date+'"', '-p=' + image_file_name , 'new'], stdin=echo.stdout, stdout=subprocess.PIPE)
        endofpipe = dayone.stdout
        neededfortimingreasons = endofpipe.readline()

        if int(tweet['id']) > lastid:
            new_lastid = int(tweet['id'])

    if(image_file_name != ''):
        os.remove(image_file_name)


try:
    lastid_file = open(lastid_filename, 'w')
    lastid_file.write(str(new_lastid))
    lastid_file.close()
except:
    print "Error: Could not write to " + lastid_filename