import pandas as pd
import os
import json

tables_dir = "tables"

def read_datasets():
    datasets = {}
    for path in os.listdir(tables_dir):
        filePath = os.path.join(tables_dir,path) 
        d = pd.read_table(filePath, sep="|", header=0) \
            .set_index("Source region")\
            .dropna(axis=1,how='all')\
            .iloc[1:]
        datasets[path] = d
    return datasets

def join_datasets(datasets):
    data = pd.DataFrame()
    for k,v in datasets.items():
        if (data.empty):
            data = v
            continue
        data = data.join(v)
    return data

def read_locations():
    d = pd.read_table("locations", sep="\t", comment='#') \
        .set_index("Region Name")[["Long", "Lat"]]
    return d

def main():
    ds = read_datasets()
    data = join_datasets(ds)
    data_dict = data.fillna("NaN").to_dict()
    data_filename = "templates/data.json"
    with open(data_filename,"w") as f:
        json.dump(data_dict, f)
        
    locs = read_locations()
    location_dict = locs.to_dict("index")
    location_filename = "templates/location.json"
    with open(location_filename,"w") as f:
        json.dump(location_dict, f)

main()