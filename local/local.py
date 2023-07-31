
import requests
import socketio


# 服务器地址
server_url = 'http://your_server_ip:5000/send_data'

# 要发送的数据
data = {"key": "value"}

# 发送POST请求
response = requests.post(server_url, json=data)

# 获取服务器的响应
if response.status_code == 200:
    result = response.json()
    print(result['message'])
else:
    print("Failed to communicate with the server.")


# 创建SocketIO客户端实例
sio = socketio.Client()

# 连接到服务器
sio.connect('http://your_server_ip:5000')

# 服务器发送消息的回调函数
@sio.on('client_message')
def handle_client_message(message):
    print("Received message from server:", message)

# 服务器发送消息给客户端
sio.emit('server_message', {"key": "value"})

# 保持客户端运行，以便接收来自服务器的消息
try:
    while True:
        pass
except KeyboardInterrupt:
    sio.disconnect()


