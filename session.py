import os
import json

def _make_json_serializable(user):
    user = dict(user)
    if '_id' in user:
        user['_id'] = str(user['_id'])
    return user

SESSION_FILE = os.path.join(os.path.dirname(__file__), 'session.json')

def save_session(user):
    user = _make_json_serializable(user)
    with open(SESSION_FILE, 'w') as f:
        json.dump(user, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
