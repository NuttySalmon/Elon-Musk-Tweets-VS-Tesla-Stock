import GetOldTweets3 as got
import concurrent.futures
import csv
from datetime import datetime, timedelta

def getTweets(since, until):
    tweetCriteria = got.manager.TweetCriteria().setUsername("elonmusk")\
                                            .setSince(since)\
                                            .setUntil(until)\
                                            .setMaxTweets(5000)\
                                            .setEmoji("none")

    print('Getting Tweets {} to {}'.format(since, until))
    return got.manager.TweetManager.getTweets(tweetCriteria)

tweets = list()
dates = [["2020-04-26", "2020-04-27"], ["2020-04-26", "2020-04-27"], ["2020-04-26", "2020-04-27"]]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    zipped_pairs = zip(*dates)
    starts, ends = zipped_pairs
    results = executor.map(getTweets, starts, ends)
    for result in results:
        tweets.extend(result)

if len(tweets) == 0:
    print('No tweets found.')
else:    
    print('Got tweets, generating csv...')
    fieldnames = tweets[0].__dict__.keys() # get header

    # write data to csv
    with open('tweets.csv', mode='w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet.__dict__)

print('Done!')