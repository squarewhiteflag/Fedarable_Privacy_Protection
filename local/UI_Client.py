import tkinter as tk
from tkinter import messagebox
import requests
import getpass
import hashlib
import json
import random
import numpy as np
from PIL import Image, ImageTk

# 假设服务器的基本URL已经设定好了
BASE_URL = "http://localhost:5000/"
V = [1, 2, 3, 4, 5, 6, 7]  # 示例梯度V
A, m, n = None, None, None  # 初始化A, m, n

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

def get_A():
    global A, m, n
    try:
        response = requests.post(BASE_URL + '/getA')
        if response.status_code == 200:
            data = response.json()
            A, m, n = data['A'], data['m'], data['n']
            messagebox.showinfo("获取模型", "模型获取成功")
        else:
            messagebox.showerror("获取模型", "模型获取失败：" + response.text)
    except Exception as e:
        messagebox.showerror("获取模型", "请求失败：" + str(e))

def generate_A():
    if A is None or m is None or n is None:
        messagebox.showerror("上传模型", "请先获取模型参数")
        return

    try:
        e = np.random.normal(size=m, loc=1, scale=1)
        k = max(V)
        s = np.random.rand(n) % k
        b = np.dot(A, s) + e  # 矩阵A*密钥s+误差向量e
        h = V + b  # h=向量v+b 添加噪声

        response = requests.post(BASE_URL + '/shamir', json={
            'h': h.tolist(),  # 确保发送的数据格式正确
            'group_id': group_id_entry.get(),
            'num_members': num_members_entry.get(),
            'localurl': local_url_entry.get() + '/shamir1',
            'round': 1
        })

        if response.status_code == 200:
            messagebox.showinfo("上传模型", "模型上传成功")
        else:
            messagebox.showerror("上传模型", "模型上传失败：" + response.text)
    except Exception as e:
        messagebox.showerror("上传模型", "请求失败：" + str(e))

app = tk.Tk()
app.title("联邦学习医疗应用")
app.geometry('800x600')  # 设置窗口大小

# 设置背景图片
image_path = './img/test.jpg'
bg_image = Image.open(image_path)
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # 调整图片大小以适应窗口
photo_image = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(app, image=photo_image)
background_label.place(relwidth=1, relheight=1)



# 用户名和密码输入框
username_label = tk.Label(background_label, text="用户名:", bg='lightgray')
username_label.pack()
username_entry = tk.Entry(background_label)
username_entry.pack()

password_label = tk.Label(background_label, text="密码:", bg='lightgray')
password_label.pack()
password_entry = tk.Entry(background_label, show="*")
password_entry.pack()

# 获取模型和上传模型所需的输入框
group_id_label = tk.Label(background_label, text="组ID:", bg='lightgray')
group_id_label.pack()
group_id_entry = tk.Entry(background_label)
group_id_entry.pack()

num_members_label = tk.Label(background_label, text="成员数量:", bg='lightgray')
num_members_label.pack()
num_members_entry = tk.Entry(background_label)
num_members_entry.pack()

local_url_label = tk.Label(background_label, text="本地URL:", bg='lightgray')
local_url_label.pack()
local_url_entry = tk.Entry(background_label)
local_url_entry.pack()

# 注册、登录、获取模型和上传模型的按钮
register_button = tk.Button(background_label, text="注册", command=register)
register_button.pack()

login_button = tk.Button(background_label, text="登录", command=login)
login_button.pack()

get_model_button = tk.Button(background_label, text="获取模型", command=get_A)
get_model_button.pack()

upload_model_button = tk.Button(background_label, text="上传模型", command=generate_A)
upload_model_button.pack()

app.mainloop()