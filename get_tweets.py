import GetOldTweets3 as got
import concurrent.futures
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

TARGET_USERNAME = 'elonmusk'
MAX_TWEET_COUNT = 5000  # for getting tweets
DATE_STR_FORMAT = '%Y-%m-%d'
MAX_WORKER = 8  # for ThreadPoolExecutor


def get_tweets(since, until):
    """Get tweets using GetOldTweet3 module

    :param since: Begining of the time range to fetch data. Format: yyyy-mm-dd
    :type since: str
    :param until: Begining of the time range to fetch data. Format: yyyy-mm-dd
    :type until: str
    :return: Tweets fetched
    :rtype: list(GetOldTweets3.models.Tweet.Tweet)
    """
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
    """Mutithreaded function to get tweets

    :param date_ranges: Ranges of dates to get tweets from
    :type date_ranges: list(list(str, str))
    :return: Tweets fetched
    :rtype: list(GetOldTweets3.models.Tweet.Tweet)
    """
    tweets = list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        # split range pairs to 2 lists of all starts and all ends
        zipped_pairs = zip(*date_ranges)
        starts, ends = zipped_pairs

        # run fetch function with ThreadPoolExecutor
        results = executor.map(get_tweets, starts, ends)

        # combind result to single list
        for result in results:
            tweets.extend(result)

    return tweets


def write_csv(tweets, filename):
    """Write tweets fetched to a csv file

    :param tweets: Tweets fetched
    :type tweets: list(GetOldTweets3.models.Tweet.Tweet)
    :param filename: Filename of csv to be generated
    :type filename: str
    """
    print('Writing to CSV...')

    # get header from first element's attributes
    fieldnames = tweets[0].__dict__.keys()

    # write data to csv
    with open(filename, mode='w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # write csv header
        for tweet in tweets:
            writer.writerow(tweet.__dict__)  # write attributes as row


if __name__ == "__main__":
    filename = 'tweets.csv'

    # begining date
    from_date = datetime(2012, 1, 2)

    # interval to increment when generating the ranges
    interval = relativedelta(months=1)

    # how times to increment / how many time ranges to generate
    count = 100
    date_ranges = list()
    curr_start = from_date

    # set up date ranges
    for _ in range(count):
        curr_end = curr_start + interval  # with increment

        start_str = curr_start.strftime(DATE_STR_FORMAT)
        end_str = curr_end.strftime(DATE_STR_FORMAT)
        date_ranges.append([start_str, end_str])

        curr_start = curr_end  # set end as next start

    print('***Fetching tweets: {} - {}***'.format(from_date.strftime(DATE_STR_FORMAT),
                                                  curr_start.strftime(DATE_STR_FORMAT)))

    tweets = get_tweets_multithreaded(date_ranges)

    size = len(tweets)
    if size == 0:
        print("No tweets found")
    else:
        print('\n***FETCHED: {} tweets from {} to {}***\n'.format(size, from_date.strftime(DATE_STR_FORMAT),
                                                                  curr_start.strftime(DATE_STR_FORMAT)))

        write_csv(tweets, filename)
        print("Done!")
