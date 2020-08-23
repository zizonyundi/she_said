from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

# with open("templates/index.html") as fp:
#     soup = BeautifulSoup(fp, 'html.parser')
#     result = soup.find_all('p',class_="select")
#     for tag in result:
#         return tag.text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def show_sayings():
    sayings = list(db.shesaid.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'sayings_list': sayings})

@app.route('/category', methods=['GET'])
def sort_sayings():
    with open("templates/index.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        result = soup.find_all('p', class_="select")
        for tag in result:
            print(tag.text)
            sayings = list(db.shesaid.find({"category": {"$in": [tag.text]}}, {'_id': False}))
            return jsonify({'result': 'success', 'sayings_list': sayings})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

