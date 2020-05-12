from flask import Flask, request
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import requests
import json
import random

app = Flask(__name__)

WORDS = [
    'Hi',
    'Hello',
    'LOL',
    '...',
    'Yes',
    'No',
    'Bye',
    'Oh',
    'Hahaha',
    'Oh yeah',
    'Very good!',
    'Awesome!',
    'Unbelievalble',
    'WOW'
]

USER_IDS = set()

def add_user(user_id):
    if user_id not in USER_IDS:
        USER_IDS.add(user_id)

def push_message(user_id, text):
    app.config.from_pyfile("config.py")
    headers = {
        'Content-type'  : 'application/json',
        'Authorization' : 'Bearer ' + app.config['CHANNEL_ACCESS_TOKEN']
    }
    payload = {
        "to": user_id,
        "messages":[{
            "type" : "text", "text" : text
        }]
    }
    requests.post(
        'https://api.line.me/v2/bot/message/push',
        headers = headers,
        json = payload
    )

def push_messages():
    message = random.choice(WORDS)
    for user_id in USER_IDS:
        push_message(user_id, message)

@app.route("/webhook", methods=['POST'])
def rawbot():
    data = request.json
    for event in data['events']:
        if event['source']['type'] != 'user':
            pass
        else:
            user_id = event['source']['userId']
            add_user(user_id)
    push_messages()
    return "ok"


