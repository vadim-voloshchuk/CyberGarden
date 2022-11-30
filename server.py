from flask import Flask
import pandas as pd
from flask import jsonify
import sklearn
from flask import request
import json
from joblib import dump, load

app = Flask(__name__)

def get_all_fithes():
    return pd.read_csv("final_langs.csv")

@app.route("/get_fithces_all", methods=['GET'])
def index():
    data = get_all_fithes()

    print(data)

    return jsonify(data.to_json())


@app.route("/get_fithces_search", methods=['POST'])
def get_datas():
    data = get_all_fithes()
    clf = load(open("LangClassifier.pkl", "rb")) 
    res = clf.predict([request.get_json(force=True)['text']])[0]
    print(res)
    
    clf_log = load(open(f"models/{res}.pkl", "rb")) 
    res_2 = data[data['name'].apply(lambda x: x.split('/')[1]) == clf_log.predict([request.get_json(force=True)['text']])[0]]
    result = {"data":{res: [{"name": res_2["name"].to_numpy()[0], "desc": res_2["description"].to_numpy()[0], "tegs": res_2["keys"].to_numpy()[0],"link": f"https://github.com/{res_2['name'].to_numpy()[0]}" ,"stars" : res_2["stars"].to_numpy()[0]}]}}

    print(result)

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)