from flask import Flask
import os
import analise
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/")
def hello():
    return json.dumps(analise.get_candidates_bag_of_words())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

