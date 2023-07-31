from flask import Flask, request, jsonify
import csv
import os
import ipaddress
from flask import make_response
from datetime import datetime, timedelta
import requests

app = Flask(__name__)
url = "http://localhost:5000/receive_file"
url1='http://localhost:5001/receive_information'
@app.route('/receive_information', methods=['POST'])
def receive_information():
    # 从POST请求中获取数据
    data = request.get_json()
    print(f"Received data: {data}")
    return 'OK', 200

@app.route('/receive_file', methods=['POST'])
def receive_file():
    # 从POST请求中获取文件
    file_data = request.files.get('file')
    if file_data:
        with open('received_file', 'wb') as file:
            file.write(file_data.read())
        return 'OK', 200
    else:
        return 'No file in request', 400

def add_account(username, password, ip):
    filename = "accounts.csv"
    id = 0

    # 检查文件是否存在，如果存在，获取最后一行的 ID
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            last_line = list(csv.reader(f))[-1]
            id = int(last_line[0]) + 1

    # 将账户信息添加到文件中
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([id, username, password, ip])

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data['action'] == 'register':
        username = data['username']
        password = data['password']
        ip = request.remote_addr
        add_account(username, password, ip)
        return 'OK', 200
    
def is_ip_close(ip1, ip2):
    # 只比较IPv4地址的前两个数字
    return ip1.split('.')[:2] == ip2.split('.')[:2]

def get_account(username):
    # 从文件中获取账户信息
    with open('accounts.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == username:
                return row
    return None

def log_behavior(id, behavior):
    # 在日志文件中记录行为
    with open('log.txt', 'a') as f:
        f.write(f"{datetime.now()}: ID {id} {behavior}\n")


def send_information(url,data):
    
    # 发送POST请求
    response = requests.post(url, json=data)
    
    # 检查请求是否成功
    if response.status_code == 200:
        print(f"Sent data: {data}")
        return 'OK', 200
    else:
        print(f"Failed to send data: {response.status_code}")
        return 'Failed', 400
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if data['action'] == 'login':
        username = data['username']
        password = data['password']
        ip = request.remote_addr
        
        account = get_account(username)
        if account and account[2] == password:
            if not is_ip_close(ip, account[3]):
                # 将异常登录信息写入文件
                with open('suspicious_logins.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([username, ip])
                    log_behavior(account[0], "failed login attempt")
            # 创建一个带有ID cookie的响应
            resp = make_response('OK')
            expires = datetime.now()
            expires = expires + timedelta(hours=1)
            resp.set_cookie(account[0], expires=expires)
            log_behavior(account[0], "logged in")
            data1=jsonify(('login','sucessfully'))
    data1=jsonify(('login','failed'))
    return send_information(url1,data1)




if __name__ == '__main__':
    app.run(port=5000)  # 运行服务器
