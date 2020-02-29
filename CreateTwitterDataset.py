#libraries
import json
import csv
from twitterscraper import query_tweets
import datetime as dt
import re
import emoji
import time

class DataSetCreator:
    def __init__(self,DEBUG = False):
        self.DEBUG = DEBUG
        self.data_set = {} #{tweet1<String>:(emoji1,emoji2...emojiN)...}
        self.raw_data = [] #[("tweettext",emoji),...]

    def scrape_twitter(self,hashtags,date = dt.date(2006, 3, 21)):
        """
        get list of hashtags and quanities for each. download that amount of each hashtags and save to raw field
        :param hashtags:
        :return:
        """
        if self.DEBUG: print("scrape_twitter() Called")
        for hashtag in hashtags:
            print("Downloading",hashtag[1]," tweets about",hashtag[0])
            list_of_tweets = query_tweets(hashtag[0], limit = int(hashtag[1]),begindate=date)
            with open(hashtag[0]+".txt", "w",encoding="utf-8") as file: #save to temp folder
                for tweet in list_of_tweets:
                    emojies = DataSetCreator.extractEmojies(tweet)
                    file.write(tweet.text)
                    self.raw_data.append((tweet.text,emojies)) #save to raw

    def load_tweets(self,PATH):
        """
        load tweets from file
        :param hashtags: list of hashtags, loads files with corresponding file names e.g. "blabla" as hashtag will try to open file "blabla.txt"
        :return:
        """
        #instead of scrape twitter (if already downloaded)

        with open(PATH + ".txt", "r") as file:  # save to temp folder
            raw_json = file.read()
            self.data_set = json.loads(raw_json)

    def preprocDataSet(self):
        """
        runs throgh saved tweets in raw field and processes them to export format, saves them in data set field
        :return:
        """
        if self.DEBUG: print("preprocDataSet() called")
        for tweet in self.raw_data:
            if tweet[1] != "":
                self.data_set[tweet[0]] = [emoji for emoji in tweet[1]]

    def export(self,PATH):
        """
        exports data set field to Dataset file
        :param PATH:
        :return:
        """
        with open(PATH + ".txt", "w", encoding="utf-8") as file:  # save to temp folder
            file.write(json.dumps(self.data_set))
        print("data_Set at: ",len(self.data_set),"indices")

    @staticmethod
    def extractEmojies(tweet):
        raw_text = tweet.text_html
        emojies = ''.join(c for c in raw_text if c in emoji.UNICODE_EMOJI)
        return emojies


def loadHashTags(PATH):
    hashtags = []
    with open(PATH, "rt", encoding='ascii') as infile:
        read = csv.reader(infile)
        for row in read:
            hashtags.append((row[0],row[1]))
    return hashtags #[(hashtag1,quantity),...,(hashtag2,quantity)]

def example():
    #create a tweets downloader
    #download preproc and export
    hashtags = loadHashTags("hashtags_test.csv")
    print("Loaded ", len(hashtags), "hashtags.")
    my_creator = DataSetCreator(DEBUG=True)
    my_creator.scrape_twitter(hashtags)  # scrapes hashtags into raw data
    my_creator.preprocDataSet()
    my_creator.export("./results")

def scrape(begindate):
    # create a tweets downloader
    # download preproc and export
    hashtags = loadHashTags("hashtags-test.csv")
    print("Loaded ", len(hashtags), "hashtags.")
    my_creator = DataSetCreator(DEBUG=False)
    my_creator.load_tweets("./results")
    my_creator.scrape_twitter(hashtags,date=begindate)  # scrapes hashtags into raw data
    my_creator.preprocDataSet()
    my_creator.export("./results")

def infinite(duration):
    INTERVAL = 3660 #3660 = 1:01 hours  #<<<<>>>>> DEBUG
    duration = duration * 24 * 60 * 60 #in seconds
    time_left = duration
    begindate = dt.date(2018, 3, 21)
    start = time.time()
    flag,printed = True,False
    while time_left > 0:
        elapsed = int(time.time() - start)
        time_left = duration - elapsed
        if elapsed % INTERVAL == 0 and flag:
            print("\n--------------")
            itr_started = time.time()
            print("downloading begin_date:",begindate)
            scrape(begindate)
            begindate += dt.timedelta(days=10) #advance 10 days in history
            flag = False
            print("iter finished after:",int(time.time() - itr_started),"seconds")
            print("\n-------------")
        elif elapsed % INTERVAL != 0:
            flag = True
        if elapsed % 2 == 0 and printed == False:
            elapsed = int(time.time() - start)
            print("\rtime left for next iter:",int(INTERVAL - elapsed % INTERVAL),"seconds",end="")
            printed = True
        elif elapsed % 2 == 1:
            printed = False


def main():
    infinite(10) #run for X time, in days

if __name__ == "__main__":
    main()