import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import hashlib

# 假设服务器的基本URL已经设定好了
BASE_URL = "http://localhost:5000/"

def register():
    url = BASE_URL + 'register'
    username = username_entry.get()
    password = password_entry.get()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        response = requests.post(url, json={'action': 'register', 'username': username, 'password': password_hash})
        if response.status_code == 200 and response.text == 'OK':
            messagebox.showinfo("注册", "注册成功")
        else:
            messagebox.showerror("注册", "注册失败：" + response.text)
    except Exception as e:
        messagebox.showerror("注册", "请求失败：" + str(e))

def login():
    url = BASE_URL + 'login'
    username = username_entry.get()
    password = password_entry.get()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        response = requests.post(url, json={'action': 'login', 'username': username, 'password': password_hash})
        if response.status_code == 200:
            messagebox.showinfo("登录", "登录成功")
        else:
            messagebox.showerror("登录", "登录失败：" + response.text)
    except Exception as e:
        messagebox.showerror("登录", "请求失败：" + str(e))

app = tk.Tk()
app.title("网络请求应用")
app.geometry('800x600')  # 设置窗口大小

# 设置背景图片
image_path = './img/test.jpg'
img = Image.open(image_path)
img = img.resize((800, 600), Image.Resampling.LANCZOS)  # 调整图片大小以适应窗口
photo = ImageTk.PhotoImage(img)
background_label = tk.Label(app, image=photo)
background_label.place(relwidth=1, relheight=1)  # 使背景图片填满窗口

# 用户名和密码输入框
username_label = tk.Label(background_label, text="用户名:", bg="lightblue")
username_label.pack()
username_entry = tk.Entry(background_label)
username_entry.pack()

password_label = tk.Label(background_label, text="密码:", bg="lightblue")
password_label.pack()
password_entry = tk.Entry(background_label, show="*")
password_entry.pack()

# 注册、登录按钮
register_button = tk.Button(background_label, text="注册", command=register)
register_button.pack()

login_button = tk.Button(background_label, text="登录", command=login)
login_button.pack()

app.mainloop()
