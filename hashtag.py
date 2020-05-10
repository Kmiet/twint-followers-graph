import tweepy
import sys
import jsonpickle
import pandas as pd 
import json

auth = tweepy.OAuthHandler('2l5EsCB5xoR5X1QXM7Vllevu8', 'NuN25ZASb37sDGHhgw8DhHr99hzPjN4IrH25oDAlWKr8uWZCZP')
auth.set_access_token('1233360710794698752-sAAVzLUsFHzMxzOjxFUcDfJkCZTIXM', 'kVTQ7PY2D4XH3UAMIfKTfZssXOh79zNImWmuVHdRc6SST')

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
maxTweets = 200

tweetCount = 0

start_username = ""
after_start_username = True

COM = 31

fName = 'smaller100k_mention_comm_%s.txt' % COM
datContent = [i for i in open("./user_comm/smaller100k_mention_comm.txt").readlines()]
user_names = []
hashtags = dict()

for i in datContent:
    _com, _unames = i.split(' ', 1)
    com = int(_com)
    if com == COM:
        unames = json.loads(_unames)

        for u in unames:

            if after_start_username:    
                user_names.append(u)

            if u == start_username:
                after_start_username = True

for i in user_names:
    print('proceeding:', user_names.index(i),'/',len(user_names))
    searchQuery = '@' + i
    print(searchQuery)
    q=searchQuery+retweet_filter
    q = searchQuery
    tweetCount = 0
    max_id = -1

    while tweetCount < maxTweets:
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
                htags = tweet._json['entities']['hashtags']
                for _h in htags:
                    h = _h['text']
                    if not hashtags.get(h):
                        hashtags[h] = 0

                    hashtags[h] += 1

            tweetCount += len(new_tweets)
            print(tweetCount)
            max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            # Just exit if any error
            # print("some error : " + str(e))
            break
                
with open('./hashtags/%s' % fName, 'w+') as f:
    f.write(json.dumps(hashtags))