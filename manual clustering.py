import csv
import json

def loadManualCluster(PATH):
    cluster_set = {}
    with open(PATH, encoding="utf-8") as csv_file:     #load file
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader: # go over each row
            emoji_utf = row[0].strip()
            emoji_cat = row[2]
            cluster_set[emoji_utf] = emoji_cat
    #add utf as key, group as value
    print("cluster set loaded")
    return cluster_set

def loadExistingDB(PATH):
    with open(PATH, encoding="utf-8") as file:
        DB = json.loads(file.read())#load json
    print("DB loaded")
    return DB

def translateDB(origin,translation_set):
    translated_db = {}
    for key,val in origin.items(): # go over each value
        if translation_set.get(val) != None:
            translated_db[key] = translation_set[val]
        else: # else put uncategorized
            translated_db[key] = "unlisted_category"
    print("DB translated")
    return translated_db

def exportDB(DB,PATH):
    with open(PATH,"w+",encoding="utf-8") as file:#export DB file
        file.write(json.dumps(DB))
    print("clustered DB exported")

def main():
    cluster_set = loadManualCluster("./manual_emoji_clustering.csv")
    origin_db = loadExistingDB("./united_results.txt")
    translated_db = translateDB(origin_db,cluster_set)
    exportDB(translated_db,"clustered_results.txt")

if __name__ == "__main__":
    main()