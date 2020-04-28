import GetOldTweets3 as got
import csv
tweetCriteria = got.manager.TweetCriteria().setUsername("elonmusk")\
                                           .setSince("2010-04-26")\
                                           .setUntil("2020-04-27")\
                                           .setMaxTweets(10000)\
                                           .setEmoji("none")

print('Getting Tweets...')
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
if len(tweets) <= 0:
    print('No tweets found.')
else:
    print('Got tweets, generating csv...')
    fieldnames = tweets[0].__dict__.keys()
    with open('tweets.csv', mode='w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet.__dict__)
print('Done!')