from main import app
from flask import request
import functions as fun

@app.route('/')
def home():
    # mess = fun.s3Upload('requirements.txt', 'big.txt')
    # print(mess)
    # mess = fun.s3Delete('stegosaurus', 'big.txt')
    # print(mess)
    return "Hello world!"

@app.route('/hello/<name>', methods=['GET'])
def user(name):
    return f"Hello {name}!"

@app.route('/post', methods=['POST'])
def testPost():
    data = request.get_data()
    print(data)
    # data = request.get_json()
    # print(data)
    return data

@app.route('/<num1>/<num2>')
def process(num1, num2):
    newNum = fun.addNums(int(num1), int(num2))
    return f"{newNum}"