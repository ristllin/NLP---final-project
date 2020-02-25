#libraries
import json
import csv
from twitterscraper import query_tweets

class DataSetCreator:
    def __init__(self,DEBUG = False):
        self.DEBUG = DEBUG
        self.data_set = [] #{tweet1<String>:(emoji1,emoji2...emojiN)...}
        self.raw_data = []

    def scrape_twitter(self,hashtags):
        if self.DEBUG: print("scrape_twitter() Unsupported")
        for hashtag in hashtags:
            print("Downloading",hashtag[1]," tweets about",hashtag[0])
            list_of_tweets = query_tweets(hashtag[0], int(hashtag[1]))
            with open(hashtag[0]+".txt", "w",encoding="utf-8") as file: #save to temp folder
                for tweet in list_of_tweets:
                    file.write(tweet.text)
                    self.raw_data.append(tweet) #save to raw

    def load_tweets(self,hashtags):
        #instead of scrape twitter (if already downloaded)
        self.raw_data = []
        for hashtag in hashtags:
            with open(hashtag[0] + ".txt", "r") as file:  # save to temp folder
                self.raw_data += file.readlines() #save to raw

    def preprocDataSet(self):
        if self.DEBUG: print("preprocDataSet() Unsupported")
        for tweet in self.raw_data:
            break#<<<>>>>

    def export(self,PATH):
        if self.DEBUG: print("export() Unsupported")
        #

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