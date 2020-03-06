import re
import json

def transformToSingle(PATH,EXPORTPATH,INCLUDEPATH=None):
    corrupt = 0
    if INCLUDEPATH != None: #add to existing dict
        with open(PATH, 'r') as file:  # read file from path, load json
            included_dict_raw = file.read()
            new_format_dict = json.loads(included_dict_raw)
    else:
        new_format_dict = {} #create new dict`
    with open(PATH,'r') as file: #read file from path, load json
        original_format_dict_raw = file.read()
        original_format_dict = json.loads(original_format_dict_raw)

    for key in original_format_dict: #go over each key)
        p_start = re.compile("<<<")  # search in key <<< and >>>
        p_end = re.compile(">>>") #search in key <<< and >>>
        starting_locations = []
        ending_locations = []
        for m in p_start.finditer(key):
            starting_locations.append(m.start())
        for m in p_end.finditer(key):
            ending_locations.append(m.start())
        if len(starting_locations) != len(ending_locations) or len(starting_locations) == 0:
            corrupt += 1
            continue

        former = 0
        for i in range(len(starting_locations)): #for every <<< and >>> zipped locations
            emoji = key[starting_locations[i]+3:ending_locations[i]]
            new_key = key[former:starting_locations[i]-1]
            if emoji == "" or new_key == "":
                # corrupt+=1
                continue
            else:
                new_format_dict[new_key] =  emoji#cut from key partial sentence and save with value between <<< and >>> locations
                # print("text:",new_key)
                # print("emoji:",emoji)
            former = ending_locations[i]+3

    print("Finished, exporting to file.",len(new_format_dict),"sentences")
    print(corrupt,'/',len(original_format_dict),"sentences not in format")
    with open(EXPORTPATH,"w") as export_file:     #export new dict
        export_file.write(json.dumps(new_format_dict))

transformToSingle("results2.txt","results_6_3.txt","resultsFormat2.txt")