from flask import Flask
from flask import render_template
import json
import requests

app = Flask(__name__)

surfchecks_endpoint = 'http://localhost:5001/surfchecks'


@app.route("/")
def surfcheck():
    r = requests.get(surfchecks_endpoint)
    if (r.status_code != 200):
        raise "errrrr"
    docs = r.json()['wave_data']
    # return render_template('surfcheck.html', titre="Surfcheck mate", docs=docs)
    return render_template('surfcheck.html', titre="Surfcheck mate", docs=docs)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
