import json
import matplotlib.pyplot as plt
import numpy as np

def emojiDistribution(DB):
    counter_db = {}
    for tweet,emoji in DB.items():
        if counter_db.get(emoji) == None:
            counter_db[emoji] = 1
        else:
            counter_db[emoji] += 1
    return counter_db

def distributionMass(counter_DB):
    disribution_DB = {}
    for emoji,count in counter_DB.items():
        if disribution_DB.get(count) == None:
            disribution_DB[count] = 1
        else:
            disribution_DB[count] += 1
    return disribution_DB

def plot_dict_hist(dist_DB):
    width = 1.0  # gives histogram aspect to the bar diagram
    plt.bar( dist_DB.values(), dist_DB.keys(),width, color='g')
    plt.show()

def loadDB(PATH):
    with open(PATH,"r",encoding="utf-8") as file:
        DB = json.loads(file.read())
    return DB

def printDB(counter_DB,threshold):
    for emoji, count in counter_DB.items():
        if count >= threshold:
            print(emoji,"\t",emoji.encode('utf-8'))

def main():
    DB = loadDB("united_results.txt")
    print(len(DB),"tweets.")
    counter_DB = emojiDistribution(DB)
    print(len(counter_DB),"different emojies.")
    dist_DB = distributionMass(counter_DB)
    # plot_dict_hist(dist_DB) <<<<show hist>>>>
    count = [count for emoji, count in sorted(counter_DB.items(), key=lambda item: item[1])]
    percent = 1 - 0.10
    percentile = count[int(len(count)*percent):]
    print(round((1-percent)*100) ,"%, are ",len(percentile),"emojies, represent",round(sum(percentile)*100/len(DB),2),"percent of the tweets")
    printDB(counter_DB,count[-len(percentile)])

if __name__ == "__main__":
    main()
