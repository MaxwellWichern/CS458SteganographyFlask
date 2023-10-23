from main import app
from flask import request
import numpy as np
import functions as fun


@app.route('/')
def home():
    return "Hello world!"

@app.route('/hello/<name>', methods=['GET'])
def user(name):
    return f"Hello {name}!"

@app.route('/post', methods=['POST'])
def testPost():
    data = request.form
    file = request.files['file']
    print(data['Hidden'])
    file.save('test.jpg')
    return 'Done', 204

@app.route('/<num1>/<num2>')
def process(num1, num2):
    newNum = fun.addNums(int(num1), int(num2))
    return f"{newNum}"