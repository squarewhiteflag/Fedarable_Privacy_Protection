from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive_information', methods=['POST'])
def receive_information():
    # 从POST请求中获取数据
    data = request.get_json()
    print("Received data: ")
    print(data)
    return 'OK', 200

if __name__ == "__main__":
    app.run(port=5001)
