from flask import Flask, render_template
from flask_cors import CORS
import pandas as pd
import os

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
    #print(d)
    return d

def main():
    read_locations()
    datasets = read_datasets()
    data = join_datasets(datasets)
    print(data)
    print(data.to_json())

ds = read_datasets()
data = join_datasets(ds)
data_dict = data.fillna("NaN").to_dict()

app = Flask(__name__)
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/latency")
def latency():
    return data_dict

locs = read_locations()
location_dict = locs.to_dict("index")

@app.route("/locations")
def locations():
    return location_dict

@app.route("/")
def index():
    return render_template("index.html")

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



    
main()