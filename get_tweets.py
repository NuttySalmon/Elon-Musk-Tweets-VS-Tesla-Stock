import GetOldTweets3 as got
import concurrent.futures
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

TARGET_USERNAME = 'elonmusk'
MAX_TWEET_COUNT = 5000
DATE_STR_FORMAT = '%Y-%m-%d'
MAX_WORKER = 8


def get_tweets(since, until):
    tweetCriteria = got.manager.TweetCriteria().setUsername(TARGET_USERNAME)\
        .setSince(since)\
        .setUntil(until)\
        .setMaxTweets(MAX_TWEET_COUNT)\
        .setEmoji("none")

    print('Getting tweets {} to {}'.format(since, until))
    results = got.manager.TweetManager.getTweets(tweetCriteria)
    print('Got tweets for {} to {}'.format(since, until))
    return results


def get_tweets_multithreaded(date_ranges):
    tweets = list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        # Start the load operations and mark each future with its URL
        zipped_pairs = zip(*date_ranges)
        starts, ends = zipped_pairs
        results = executor.map(get_tweets, starts, ends)
        for result in results:
            tweets.extend(result)

    return tweets


def write_csv(tweets, filename):
    fieldnames = tweets[0].__dict__.keys()  # get header

    # write data to csv
    with open(filename, mode='w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet.__dict__)


if __name__ == "__main__":
    filename = 'tweets.csv'
    from_date = datetime(2016, 1, 1)
    interval = relativedelta(months=1)
    count = 46
    date_ranges = list()
    curr_start = from_date

    # set up date ranges
    for _ in range(count):
        curr_end = curr_start + interval
        start_str = curr_start.strftime(DATE_STR_FORMAT)
        end_str = curr_end.strftime(DATE_STR_FORMAT)
        date_ranges.append([start_str, end_str])
        curr_start = curr_end

    print("RANGE: {} - {}".format(from_date.strftime(DATE_STR_FORMAT),
                                  curr_start.strftime(DATE_STR_FORMAT)))
    tweets = get_tweets_multithreaded(date_ranges)
    write_csv(tweets, filename)
