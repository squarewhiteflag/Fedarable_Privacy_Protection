import requests
import getpass
import hashlib
from requests.exceptions import Timeout

url = "http://localhost:5000/receive_information"

def send_information_to_server(url, data):
    # url是服务器地址，data是要发送的信息
    response = requests.post(url, json=data)
    return response.status_code, response.text

def send_file_to_server(url, file_path):
    # url是服务器地址，file_path是要发送的文件路径
    with open(file_path, 'rb') as file:
        file_data = file.read()
    response = requests.post(url, files={'file': file_data})
    return response.status_code, response.text


def register(url):
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    # 使用 SHA-256 哈希算法对密码进行加密
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    response_code, response_text = send_information_to_server(url, {'action': 'register', 'username': username, 'password': password_hash})

    if response_code == 200 and response_text == 'OK':
        print("Registration successful")
    else:
        print("Registration failed")


def login(url):
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    response_code, response_text = send_information_to_server(url, {'action': 'login', 'username': username, 'password': password_hash})
    print('request: '+response_text)



def main():
    url = "http://localhost:5000/receive_information"

    while True:
        print("Please choose an action:")
        print("1. Register")
        print("2. Login")
        print("3. Quit")

        choice = input()

        if choice == '1':
            register(url)
        elif choice == '2':
            login(url)
        elif choice == '3':
            break
        else:
            print("Invalid choice, please choose again.")

if __name__ == "__main__":
    main()
