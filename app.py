from flask import Response, Flask, render_template
from flask_socketio import SocketIO, emit
from controllers import Controller
from data import dao

app = Flask(__name__)
app.config['SECRETKEY'] = "secret"
socketIo = SocketIO(app)

arduinoEndpoint = dao.ArduinoEndpoint("Arduino Access Endpoint")
userDAO = dao.UserDAO("User Info Access Object")
controller = Controller(arduinoEndpoint)

def tempEvent():
    for x in arduinoEndpoint.serialOut():
        print(x)
        yield "data"+  x

@app.route('/stream')
def data_stream():
    return Response(tempEvent(), mimetype="text/event-stream")

@app.route('/')
def index():
    return render_template('index.html')


@socketIo.on('my_event')
def handle_custom_event(data):
    emit("a response: ", data, broadcast=True)

if __name__ == '__main__':
    socketIo.run(app)
