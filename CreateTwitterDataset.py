#libraries
import json
import csv
from twitterscraper import query_tweets
import datetime as dt
import re
import emoji

class DataSetCreator:
    def __init__(self,DEBUG = False):
        self.DEBUG = DEBUG
        self.data_set = [] #{tweet1<String>:(emoji1,emoji2...emojiN)...}
        self.raw_data = [] #[("tweettext",emoji),...]

    def scrape_twitter(self,hashtags,date = dt.date(2006, 3, 21)):
        """
        get list of hashtags and quanities for each. download that amount of each hashtags and save to raw field
        :param hashtags:
        :return:
        """
        if self.DEBUG: print("scrape_twitter() Unsupported")
        for hashtag in hashtags:
            print("Downloading",hashtag[1]," tweets about",hashtag[0])
            list_of_tweets = query_tweets(hashtag[0], limit = int(hashtag[1]),begindate=date)
            with open(hashtag[0]+".txt", "w",encoding="utf-8") as file: #save to temp folder
                for tweet in list_of_tweets:
                    emojies = DataSetCreator.extractEmojies(tweet)
                    file.write(tweet.text)
                    self.raw_data.append((tweet,emojies)) #save to raw

    def load_tweets(self,hashtags):
        """
        load tweets from file
        :param hashtags: list of hashtags, loads files with corresponding file names e.g. "blabla" as hashtag will try to open file "blabla.txt"
        :return:
        """
        #instead of scrape twitter (if already downloaded)
        self.raw_data = []
        for hashtag in hashtags:
            with open(hashtag[0] + ".txt", "r") as file:  # save to temp folder
                self.raw_data += file.readlines() #save to raw

    def preprocDataSet(self):
        """
        runs throgh saved tweets in raw field and processes them to export format, saves them in data set field
        :return:
        """
        if self.DEBUG: print("preprocDataSet() Unsupported")
        for tweet in self.raw_data:
            if tweet[1] != "":
                self.data_set.append({tweet[0],[emoji for emoji in tweet[1]]})

    def export(self,PATH):
        """
        exports data set field to Dataset file
        :param PATH:
        :return:
        """
        print(self.data_set)
        with open(PATH + ".txt", "w", encoding="utf-8") as file:  # save to temp folder
            file.write(json.dumps(self.data_set))

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

def main():
    hashtags = loadHashTags("hashtags_test.csv")
    print("Loaded ",len(hashtags),"hashtags.")
    my_creator = DataSetCreator(DEBUG = True)
    my_creator.scrape_twitter(hashtags) #scrapes hashtags into raw data
    my_creator.preprocDataSet()
    my_creator.export("MyDataSet.csv")

if __name__ == "__main__":
    main()