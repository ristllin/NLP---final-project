import re
import csv
import pandas as pd
import json

def merge_csvs(csv1, csv2):
    """
    Merge two Tweets Emojies data base into one csv file.
    :param: csv1 - first tweet to emojies db
            csv2 - second tweet to emojies db
    :return: None
    """
    csv1_data = pd.read_csv(csv1)
    csv2_data = pd.read_csv(csv2)
    csv1_label_fields = list(csv1_data.columns.values)
    csv1_label_fields.pop(0)
    csv2_label_fields = list(csv2_data.columns.values)
    csv2_label_fields.pop(0)
    labels = set(csv1_label_fields)
    labels.update(csv2_label_fields)
    file = open('merged_tweets_emojies.csv', 'w')
    with file:
        fields = ['tweet'] + list(labels)
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for tweet in csv1_data['tweet']:
            line = {'tweet': tweet}
            for label in labels:
                if label in csv1_label_fields:
                    line[label] = csv1_data[label]
                else:
                    line[label] = 0
            writer.writerow(line)
        for tweet in csv2_data['tweet']:
            line = {'tweet': tweet}
            for label in labels:
                if label in csv2_label_fields:
                    line[label] = csv2_data[label]
                else:
                    line[label] = 0
            writer.writerow(line)
    file.close()

def dictToCSV(PATH,EXPORTPATH):
    with open(PATH, 'r',encoding="utf-8") as content_file:
        data_raw = content_file.read()
        data = json.loads(data_raw)
    print(">>>Convertion Started")
    # count = 1
    emojies_in_data = set()
    for val in data.values(): emojies_in_data.add(val)
    fields = ['tweet'] + list(emojies_in_data)
    print("loaded:",len(fields),"fields")
    with open(EXPORTPATH, 'w',encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for tweet,emoji in data.items():
            # if count % 10 == 0:
                # print("\rConverted: ",count,"/",len(data),end="")
            # count += 1
            line = {'tweet': tweet}
            for label in fields:
                if label == emoji:
                    line[label] = 1
                else:
                    line[label] = 0
            writer.writerow(line)
    print("\n>>>Finished successfully")

def Run():
    """
    parse results.txt and creats a csv file `tweets_emojies.csv` which contains fields as tweets and all type of emojies
    Make sure to have results.txt ready to parse in the containing directory
    :param: None
    :return: None
    """
    with open('results.txt', 'r') as content_file:
        text = content_file.read()
        tweets = re.compile(r"\],").split(text)
        labels = set()
        tweetsToemojies = {}
        for tweet in tweets:
           tweet = tweet.strip()
           pos = tweet.find(": [")
           emojies=tweet[pos+3:].split(",")
           emojies = set([s.strip().replace('\"', '') for s in emojies])
           labels.update(emojies)
           tweet = tweet[1:pos-1].replace('"', '').strip().strip('\"').lstrip('\"').strip('\'').lstrip('\'')
           tweetsToemojies[tweet]= emojies
        file = open('tweets_emojies.csv', 'w')
        with file:
            fields = ['tweet']+list(labels)
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for tweet,emojies in tweetsToemojies.items():
                line = {'tweet': tweet}
                for label in labels:
                    if label in emojies:
                        line[label] = 1
                    else:
                        line[label] = 0
                writer.writerow(line)
        file.close()



##############################################
if __name__ == '__main__':
    dictToCSV('results.txt','tweets_emojies.csv')