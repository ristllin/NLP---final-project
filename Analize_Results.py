import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import csv

def AnalizeResults(PATH):
    """
    shows a binary heat map of the algorithms and their success zones
    :param PATH:
    :return:
    """
    sns.set()
    algo_results = pd.read_csv(PATH).sort_values(by=['BERT','RNN','CNN','KNN']).transpose()# Simulated_Data_sample
    f, ax = plt.subplots(figsize=(15, 9))
    sns.heatmap(algo_results, linewidths=0.0 , annot=False, fmt="d", ax=ax, cmap = "Blues")
    plt.xlabel("Tweets")
    plt.ylabel("Algorithms")
    plt.show()

def loadData(PATH,csv_delimiter=','):
    """
    gets PATH to a CSV file, returns Data in relevant format
    :param PATH: <String>
    :return: <list> data [[<String>Tweet,[0,0,1,0]]...] and <list> Algorithm names in correlating order ["RNN","CNN","KNN","BERT"]
    """
    data = []
    with open(PATH,"r") as csv_file:
        file = csv.reader(csv_file, delimiter=csv_delimiter,quotechar='"')
        titles = next(file)[1:]
        print(titles)
        for line in file:
            data.append([line[0],line[1:]])
    return data,titles


def analyzeSuccessRate(Data,algorithm_names):
    """
    ranks algorithms success rates
    :param Data: <List> [[<String>Tweet,[0,0,1,0]]...]
    :param algorithm_names: <List> ["RNN","CNN","KNN","BERT"]
    :return: <List> algo_suc_rates [["CNN":0.1],["RNN":0.35],["KNN":0.1],["BERT":0.55]
    """
    algo_suc_rates =  [[alg_name,0] for alg_name in algorithm_names]
    for tweet in Data:
        suc_algs = tweet[1]
        for alg_index in range(len(algorithm_names)):
            if int(suc_algs[alg_index]) == 1:
                algo_suc_rates[alg_index][1] += 1
    for alg in algo_suc_rates: #normalize
        alg[1] = alg[1]/len(Data)
    return algo_suc_rates

def addDefault(Data,algo_suc_rates):
    """
    gets data in order to leave no blank indices, it marks all of the blank indices (where non succeeded) as successful in the dominant algorithm
    :return: <List> same format as Data but no blanks (0,0,0,0) [(<String>Tweet,[0,0,1,0])...]
    """
    Blankless_Data = []
    FULL_OPTS = ["1" for i in range(len(Data[0][1]))]
    NO_OPTS = ["0" for i in range(len(Data[0][1]))]
    dominant_index = maxAlgo(algo_suc_rates,FULL_OPTS)
    for tweet in Data:
        if tweet[1] == NO_OPTS:
            tweet[1][dominant_index] = 1
    return Data

def maxAlgo(algo_suc_rates,options):
    """
    gets list of algorith success rates and which of them are optional (in another list), returns the one with the highest success rate
    :param algo_suc_rates: <List>  [['BERT', 0.0], ['RNN', 0.5], ['CNN', 0.21428571428571427], ['KNN', 0.07142857142857142]]
    :param options: <List> ["0","1","0","1"]
    :return: <int> - index of an algo
    """
    max = 0
    max_index = -1
    for option in range(len(options)):
        if int(options[option]) == 1 and algo_suc_rates[option][1] > max: #successful option and better than previous
            max = algo_suc_rates[option][1]
            max_index = option
    if max_index == -1: #all failed
        max_index = maxAlgo(algo_suc_rates,["1","1","1","1"]) #choose the one with highest score
    return(max_index)

def labelTweets(data,algo_suc_rates,EXPORT_PATH,CSV_DELIMITER=","):
    """
    gets data and algo_suc_rates.
    builds DB as tweet:name of successful algorithm. if more than 1, puts the one with the highest success rate
    :param Data:
    :param algo_suc_rates:
    :return:
    """
    labeled_data = []
    for tweet in data:
        dominant_alg = maxAlgo(algo_suc_rates,tweet[1])
        labeled_data.append([algo_suc_rates[dominant_alg][0],tweet[0]])
    with open(EXPORT_PATH,"w",newline='') as export_file:
        csv_writer = csv.writer(export_file)
        csv_writer.writerows(labeled_data)

def labelForAWS(IMPORTPATH,EXPORTPATH):
    print(">>> Loading Data")
    data,alg_names = loadData(IMPORTPATH)
    print(">>> Calculating success rates")
    algo_suc_rates = analyzeSuccessRate(data,alg_names)
    print("Original Success rates: ",algo_suc_rates)
    print(">>> Adding default to blanks")
    data = addDefault(data,algo_suc_rates)
    algo_suc_rates = analyzeSuccessRate(data, alg_names) #unnecessary
    print("Processed Success rates: ", algo_suc_rates)
    print(">>> labeling tweets by most dominant solver")
    labelTweets(data,algo_suc_rates,EXPORTPATH)

def main():
    # AnalizeResults("./Simulated_Data.csv")
    labelForAWS("./Simulated_Data1000.csv","labeled_results.csv")

if __name__ == "__main__":
    main()
