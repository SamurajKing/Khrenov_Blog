# coding=utf-8
from flask_login import current_user
from flask_socketio import send
from unidecode import unidecode
from app import app, socket_io, db
from app.models import Message
import unicodedata

def is_good(msg):
    cur_msg = unicodedata.normalize('NFD', msg)
    cur_msg = cur_msg.replace(r'[\u0300-\u036f]/g', "")
    print("trying to send: ", cur_msg)
    cur_msg = cur_msg.strip(' ')
    cur_msg = unidecode(cur_msg)
    return len(cur_msg) > 0 and len(cur_msg) <= 255

@socket_io.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    final_msg = "<span style='color: " + current_user.roleColor + ";'>" + current_user.username + "</span>: " + msg
    current_message = Message(author=current_user, text=msg)
    if (is_good(msg)):
        db.session.add(current_message)
        db.session.commit()
        send(final_msg, broadcast=True)

if __name__ == "__main__":
    socket_io.run(app, host='0.0.0.0', port=80, debug=True)
    
