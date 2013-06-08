tweet-dayone
============

A python script to add your tweets to the Day One journalling program for OS X. Relies on the [Day One CLI](http://dayoneapp.com/tools/).

Make sure to set the following options before running:
  * lastid_filename: a text file to store the id of the last tweet we found
  * twitter_username: your twitter username
  * tweet_count: how many tweets to pull down at a time, the higher the number the less frequently you should run the script
  * retweets: 1 to include retweets and 0 to exclude them. Retweets are included in the tweet_count total no matter what you pick here
  * tweet_photos: 1 if you want to include photos from tweets in the Day One entries

The script will create a text file to store the id of the newest tweet it's added to Day One, to prevent adding duplicate tweets. It will also create temporary image files to import your photos into your Day One entries. Both of these are created in the directory you run the script from.

## Todo:
  * Incorporate timezone differences
  * Also include the original tweet if replying (done)? And retweets (check)? Favourited tweets (requires auth, I think)? Import pictures (done)? Imagining my voice is increasing in pitch with each subsequent question?
  * Should probably be using twitter's 1.1 api