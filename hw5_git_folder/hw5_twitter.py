from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk


## SI 206 - HW
## COMMENT WITH:
## Your section day/time: 005/ M 1-2:30
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
print("USER: {}".format(username))
num_tweets = sys.argv[2]
print("TWEETS ANALYZED: {}".format(num_tweets))

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends


#Write your code below:
#Code for Part 3:Caching

# initializing CACHE dictionary
CACHE_FNAME = "twitter_cache.json"
try:
    fname = open(CACHE_FNAME, 'r')
    json_data = fname.read()
    CACHE_DICTION = json.loads(json_data)
    fname.close()
except:
    CACHE_DICTION = {}

def sorted_search_params(baseurl, auth, params):
    sorted_params = sorted(params.keys())
    acc = []
    for item in sorted_params:
        acc.append("{}-{}".format(item, params[item]))
    return baseurl + "_".join(acc)

def fetch_from_twitter(screen_name, count = 20):
    baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
    params = {}
    params["screen_name"] = screen_name
    params["count"] = count
    search_id = sorted_search_params(baseurl, auth = auth, params = params)
    if search_id in CACHE_DICTION:
        print("Returning data from cache file")
        return CACHE_DICTION[search_id]
    else:
        response = requests.get(baseurl, auth= auth, params = params)
        print("Getting fresh data from Twitter")
        twitter_data = json.loads(response.text)
        CACHE_DICTION[search_id] = twitter_data
        fname = open(CACHE_FNAME, 'w')
        fname.write(json.dumps((CACHE_DICTION), indent=2))
        fname.close()
        return twitter_data


#Finish parts 1 and 2 and then come back to this

# Code for Part 1:Get Tweets

data = fetch_from_twitter(username, num_tweets)



#Code for Part 2:Analyze Tweets



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
