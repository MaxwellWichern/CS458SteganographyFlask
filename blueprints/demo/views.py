from main import app
from flask import request, jsonify
import numpy as np
import functions as fun
import requests
import json
import cv2

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
    data = request.form
    file = request.files['file']
    print(data['Hidden'])
    file.save('test.jpg')
    return 'Done', 204

@app.route('/<num1>/<num2>')
def process(num1, num2):
    newNum = fun.addNums(int(num1), int(num2))
    return f"{newNum}"