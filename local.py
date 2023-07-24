# 导入必要的模块
from flask import Flask, request

# 创建Flask应用
app = Flask(__name__)

# 本地发送信息函数框架
@app.route("/send_message", methods=["POST"])
def send_message():
    # 从请求中获取参数
    message = request.form.get("message")
    ip_address = request.form.get("ip_address")
    port = request.form.get("port")
    password = request.form.get("password")

    # 执行发送信息的逻辑
    # ...

    return "Message sent successfully"

# 本地发送文件函数框架
@app.route("/send_file", methods=["POST"])
def send_file():
    # 从请求中获取文件
    file = request.files.get("file")
    ip_address = request.form.get("ip_address")
    port = request.form.get("port")
    password = request.form.get("password")

    # 执行发送文件的逻辑
    # ...

    return "File sent successfully"


# 运行Flask应用
if __name__ == "__main__":
    app.run()
