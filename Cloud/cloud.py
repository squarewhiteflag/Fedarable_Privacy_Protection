
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# 用于接收本地发送的POST请求的路由
@app.route('/send_data', methods=['POST'])
def receive_data():
    try:
        # 获取本地发送的数据
        data = request.json

        # 在这里可以对数据进行处理
        # ...

        # 返回响应给本地
        response = {"status": "success", "message": "Data received successfully!"}
        return jsonify(response)

    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return jsonify(response), 500

# 用于接收服务器发送的消息的WebSocket事件
@socketio.on('server_message')
def handle_server_message(message):
    # 在这里可以对接收到的消息进行处理
    # ...

    # 回复服务器发送的消息
    response = {"status": "success", "message": "Message received successfully!"}
    emit('client_message', response)

if __name__ == '__main__':
    socketio.run(cloud, debug=True)


