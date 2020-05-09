import re
import csv
import pandas as pd
import json
import re
import sys
import warnings
from cucco import Cucco
import ftfy
from nltk.stem.snowball import SnowballStemmer
sbEng = SnowballStemmer('english')
sbEsp = SnowballStemmer('spanish')

# List of number terms
nums = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
        'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
        'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred',
        'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion', 'sextillion',
        'septillion', 'octillion', 'nonillion', 'decillion',
        'cero', 'uno', 'dos', 'Tres', 'cuatro', 'cinco', 'seis', 'ocho', 'nueve', 'diez', 'once',
        'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'de diecisiete', 'Dieciocho', 'diecinueve',
        'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'ochenta', 'noventa', 'cien']


def remove_numbers(s):
    """
    Removes all numbers from strings, both alphabetic (in English) and numeric. Intended to be
    part of a text normalisation process. If the number contains 'and' or commas, these are
    left behind on the assumption the text will be cleaned further to remove punctuation
    and stop-words.
    """
    digit = {str(i):'' for i in range(10)}
    query = s.replace('-', ' ').lower().split(' ')
    resultwords = [word for word in query if word not in nums]
    noText = ' '.join(resultwords).encode('utf-8')
    s = str(noText.decode("utf-8"))
    noNums = s.translate(digit).replace('  ', ' ')
    return noNums

def clean_html(sentence):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    return cleantext

def clean_punc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned

def keep_alpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

def lemmatisation(sentence):
    sent = ' '.join([sbEng.stem(item) for item in (sentence).split(' ')])
    return ' '.join([sbEsp.stem(item) for item in (sent).split(' ')])

def remove_stop_words(sentence):
    normEng = Cucco(language='en')
    normEsp = Cucco(language='es')
    norms = ['remove_stop_words', 'replace_punctuation', 'remove_extra_whitespaces']
    sent = normEng.normalize(sentence, norms)
    return normEsp.normalize(sent, norms)

def fix_encoding(sentence):
    return ftfy.fix_encoding(sentence)

def clean_csv(csv):
    csv_data = pd.read_csv(csv)
    csv_data['tweet'] = csv_data['tweet'].str.lower()
    csv_data['tweet'] = csv_data['tweet'].apply(clean_html)
    csv_data['tweet'] = csv_data['tweet'].apply(clean_punc)
    csv_data['tweet'] = csv_data['tweet'].apply(keep_alpha)
    csv_data['tweet'] = csv_data['tweet'].apply(remove_stop_words)
    csv_data['tweet'] = csv_data['tweet'].apply(remove_numbers)
    csv_data['tweet'] = csv_data['tweet'].apply(lemmatisation)
    csv_data['tweet'] = csv_data['tweet'].apply(fix_encoding)
    csv_data.to_csv('cleaned_tweet_emojie.csv', index=False)

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
            line = {'tweet': tweet, 'label':emoji}
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