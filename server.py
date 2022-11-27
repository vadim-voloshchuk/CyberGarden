from flask import Flask
import pandas as pd
from flask import jsonify
app = Flask(__name__)

def get_all_fithes():
    return pd.read_csv("final_langs.csv")

@app.route("/get_fithces_all", methods=['GET'])
def index():
    data = get_all_fithes()


    print(data)

    return jsonify(data.to_json())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)