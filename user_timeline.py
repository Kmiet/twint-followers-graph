import tweepy
import sys
import jsonpickle
import pandas as pd 
import json 


# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
auth = tweepy.OAuthHandler('CDRYVVU99qNQ2eun2qhITqAYf', 'oLigqTR1N26Ctc09oKgLRk8NexXZ3sx0z6vQfJtZVKIzdm3C68')
auth.set_access_token('1234388325894631424-JGF6oto8vmsnDkWVbcN98mvQTmonmN', 'gIYwvyY5CjDhx4ETd43tz2rWSZB9G4KOQj8eLA2zfref0')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if not api:
    print("Can't Authenticate")
    sys.exit(-1)

searchQuery = '@SzumowskiLukasz'

retweet_filter='-filter:retweets'

q=searchQuery+retweet_filter

tweetsPerQry = 200


sinceId = None
max_id = -1
# //however many you want to limit your collection to.  how much storage space do you have?
maxTweets = 1

tweetCount = 0



fName = 'mentions8_user_timeline.txt'
datContent = [i for i in open("./Users/users8.dat-kopia").readlines()]
user_names = []

for i in datContent:
    res = json.loads(i)
    user_names.append(res['username'])

import time 

start = time.time()

for i in user_names:
    print('proceeding:', user_names.index(i),'/',len(user_names))
    searchQuery = '@' + i
    print(searchQuery)
    q=searchQuery+retweet_filter
    q = searchQuery
    s = set()
    tweetCount = 0
    max_id = -1

    with open(fName, 'a+') as f:
        f.write('{"'+str(searchQuery)+'":')
        while tweetCount <= maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.user_timeline(screen_name=searchQuery, count=tweetsPerQry)
                    else:
                        new_tweets = api.user_timeline(screen_name=searchQuery, count=tweetsPerQry,
                                                since_id=sinceId)
                else:
                    if (not sinceId):
                        new_tweets = api.user_timeline(screen_name=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.user_timeline(screen_name=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
            
                    for i in tweet._json['entities']['user_mentions']:
                        s.add(i['screen_name'])


                tweetCount += len(new_tweets)
                print(tweetCount)
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                # print("some error : " + str(e))
                break
        f.write('[')
        s = list(s)
        for k in range(0, len(s)):
            if k == len(s)-1:
                f.write(str(s[k]))
            else:
                f.write(str(s[k])+",")
        f.write(']}'+'\n')
    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
    print('took:', (time.time()-start) / 60, 'm')
    
   # break


