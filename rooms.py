from gevent import monkey; monkey.patch_all()
from flask import Flask, render_template, request, json, Blueprint

from gevent import queue

rooms = Blueprint('rooms', __name__, template_folder='templates')

class Room(object):

    def __init__(self):
        self.users = set()
        self.messages = []

    def backlog(self, size=25):
        return self.messages[-size:]

    def subscribe(self, user):
        self.users.add(user)

    def add(self, message):
        for user in self.users:
            print user
            user.queue.put_nowait(message)
        self.messages.append(message)

class User(object):

    def __init__(self):
        self.queue = queue.Queue()

roomsDic = {
    'python': Room(),
    'django': Room(),
}

users = {}

@rooms.route('/rooms/choose')
def choose_name():
    return render_template('choose.html')

@rooms.route('/rooms/<uid>')
def main(uid):
    return render_template('main.html',
        uid=uid,
        rooms=roomsDic.keys()
    )

@rooms.route('/rooms/<room>/<uid>')
def join(room, uid):
    user = users.get(uid, None)

    if not user:
        users[uid] = user = User()

    active_room = roomsDic[room]
    active_room.subscribe(user)
    print 'subscribe', active_room, user

    messages = active_room.backlog()

    return render_template('room.html',
        room=room, uid=uid, messages=messages)

@rooms.route("/rooms/put/<room>/<uid>", methods=["POST"])
def put(room, uid):
    user = users[uid]
    room = roomsDic[room]

    message = request.form['message']
    room.add(':'.join([uid, message]))

    return ''

@rooms.route("/rooms/poll/<uid>", methods=["POST"])
def poll(uid):
    try:
        msg = users[uid].queue.get(timeout=10)
    except queue.Empty:
        msg = []
    return json.dumps(msg)