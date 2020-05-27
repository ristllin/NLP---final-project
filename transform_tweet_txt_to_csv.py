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
    count = 0
    with open('merged_tweets_emojies.csv', 'w',encoding="utf-8") as file:
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
            if count % 100 == 0:
                print("Converted: ", count, "/", len(csv1_data['tweet']))
            count += 1
        for tweet in csv2_data['tweet']:
            line = {'tweet': tweet}
            for label in labels:
                if label in csv2_label_fields:
                    line[label] = csv2_data[label]
                else:
                    line[label] = 0
            writer.writerow(line)
            if count % 100 == 0:
                print("Converted: ", count, "/", len(csv2_data['tweet']))
            count += 1

def removeEmojies(tweet):
    return re.sub('<<<.*?>>>', '', tweet)

def dictToCSV(PATH,EXPORTPATH):
    with open(PATH, 'r',encoding="utf-8") as content_file:
        data_raw = content_file.read()
        data = json.loads(data_raw)
    print(">>>Convertion Started")
    count = 1
    formated_data = {}
    emojies_in_data = set()
    if type(list(data.items())[0][1]) == list:
        for key,val in data.items():
            key = removeEmojies(key)
            stripped_key = strip_non_alnum(key)
            formated_data[stripped_key] = val[0]
            emojies_in_data.add(val[0])
    elif type(list(data.items())[0][1]) == str:
        for key,val in data.items():
            key = removeEmojies(key)
            stripped_key = strip_non_alnum(key)
            if type(val) == list:
                val = val[0]
            formated_data[stripped_key] = val
            emojies_in_data.add(val)
    else:
        print("unknown data structure: val of type:", type(list(data.items())[0][1]))
    fields = ['tweet'] + list(emojies_in_data)
    print(fields) #debug
    with open(EXPORTPATH, 'w',encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for tweet,emoji in formated_data.items():
            if count % 1000 == 0:
                print("Converted: ",count,"/",len(data))
            count += 1
            line = {'tweet': tweet}
            for label in fields:
                if label != "tweet":
                    if label == emoji:
                        line[label] = 1
                    else:
                        line[label] = 0
            writer.writerow(line)
    print("\n>>>Finished successfully")

def strip_non_alnum(my_string):
    my_string = re.sub('[\W_]+', ' ', my_string)
    return my_string

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
    dictToCSV('united_results.txt','united_results.csv')
    # merge_csvs('tweets_emojies1.csv', 'tweets_emojies2.csv')
