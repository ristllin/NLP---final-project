import re
import csv

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
    main()