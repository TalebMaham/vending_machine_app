from flask import Flask, render_template, jsonify
import json
import requests
from threading import Timer
from requests.auth import HTTPBasicAuth
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

items = []

def load_items():
    global items
    try:
        response = requests.get(app.config['API_URL'], auth=HTTPBasicAuth(app.config['API_USERNAME'], app.config['API_PASSWORD']))
        if response.status_code == 200:
            items = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def update_items():
    load_items()
    Timer(30, update_items).start()

@app.route('/')
def index():
    return render_template('index.html', items=items)

@app.route('/api/items')
def api_items():
    return jsonify(items)

if __name__ == '__main__':
    load_items()
    update_items()
    app.run(debug=True, port=5001)  # Port 5001
