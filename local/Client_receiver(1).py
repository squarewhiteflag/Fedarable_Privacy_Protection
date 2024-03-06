from flask import Flask, request, jsonify
import json
import requests
from nacl.public import PrivateKey, Box
import random
import shamir_sharing as shamir
import util
import galois
app = Flask(__name__)
url = "http://localhost:5000/"
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
'''
@app.route('/DH', methods=['POST'])
def recive_keys():
    received_data = request.json  # 这假设你发送的是一个JSON对象
    with open('DH.json', 'w') as f:
        json.dump(received_data, f)
    return 'OK', 200
'''
@app.route('/shamir1',methods=['post'])#收到客户端集合，发送公钥
def round2shamir():
    global num_members
    global s
    global group_id
    global localurl
    global client_id
    # 选择一个素数作为有限域的模数
    modulus = 101 
    global GF
    GF = galois.GF(modulus)
    #获取自己的ID

    with open('shamirS.json', 'r') as f:
        s = json.load(f)['s']
        num_members=json.load(f)['num_members']
        group_id=json.load(f)['group_id']
        localurl=json.load(f)['localurl']

    veryfiedurl=request.json('localurls')
    for id,url in veryfiedurl:
        if url-'/shamir1' == localurl:
            client_id = id
    global private_shamir_key
    private_shamir_key=PrivateKey.generate()
    global public_shamir_key
    public_shamir_key=private_shamir_key.public_key

    with open('key','w') as f1:
        json.dump({
            'private_key':private_shamir_key,
            'public_key':public_shamir_key},
            f1)
    response = requests.post(url+'shamir',json={
        'key':public_shamir_key,
        'group_id': group_id,
        'num_members': num_members,
        'localurl':localurl+'/shamir2',
        'round':int(2)})
    print(response)
    response_code = response.status_code

'''
def split_number(total, n):
    if n <= 0:
        raise ValueError("Number of parts n should be positive.")
    
    # 如果n为1，则直接返回整数
    if n == 1:
        return [total]
    
    # 生成n-1个随机分数点
    points = sorted([0] + [random.uniform(0, total) for _ in range(n-1)] + [total])

    # 使用这些点来计算每个部分
    parts = [points[i+1] - points[i] for i in range(n)]
    
    return parts

def split_array(numbers, n):
    # 分割每个数字
    parts_list = [split_number(num, n) for num in numbers]

    # 转置得到的部分，以便得到n个数组
    return [list(x) for x in zip(*parts_list)]


def encrypt_array_with_key(array, public_key):
    encrypted_array = []
    for item in array:
        encrypted_item = public_key.encrypt(item) # 假设公钥有一个加密方法
        encrypted_array.append(encrypted_item)
    return encrypted_array
'''
@app.route('/shamir2',methods=['post'])#得到公钥集合，发送使用自己公钥和私钥加密的每一份密钥
def round2shamir():

    global pks
    pks = request.json()#公钥集合
    n_range=list(sorted(pks.keys()))
    client_value = GF.random(low=0, high=100, size=len(s))

    # 使用Shamir's Secret Sharing算法生成秘密份额
    shares = shamir.share_array(client_value, n_range, num_members,GF)

    # 打印生成的秘密份额
    print("Generated Shares:", shares)

    enc_shares = {c: shares[c].encrypt(private_shamir_key, public_shamir_key)
                for c, pk in pks.items()
                if c in shares}

    #发送加密的秘密份额
        
    response = requests.post(url+'/shamir',json={
        's_send':enc_shares,
        'group_id': group_id,
        'num_members': num_members,
        'localurl':localurl+'/shamir3',
        'round':int(3)})
    print(response)
    response_code = response.status_code

@app.route('/shamir3',methods=['post'])#解密集合，发送解密结果
def round3shamir():
    message = request.json()
    dec_shares = [s.decrypt(private_shamir_key, pks[c])
                for c, s in message.items()
                if c in pks]
    response = requests.post(url+'/shamir',json={
        's_send':shamir.sum_share_array(dec_shares),
        'group_id': group_id,
        'num_members': num_members,
        'localurl':localurl+'/shamir3',
        'round':int(4)})
    
if __name__ == "__main__":
    app.run(port=5001)
