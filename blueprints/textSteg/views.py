from main import app
from flask import request, jsonify
import numpy as np
import functions as fun
import requests
import json
import cv2

@app.route('/user/all/images/', methods=['POST'])
def getImages():
    data = request.get_data()
    data = json.loads(data.decode())

    s3 = fun.s3Connection()
    userImages = fun.genUsersLinks(s3, data['Bucket'], data['User'], data['imType'])['Contents']
    urls = []
    for item in userImages:
        print(item['Key'])
        URL = fun.s3URL(s3, data['Bucket'], item['Key'])
        urls.append(URL)

    print(urls)
    return jsonify({'Links': urls})

@app.route('/user/upload/image/', methods=['POST'])
def uploadImage():
    data = request.get_data()
    data = json.loads(data.decode())

    s3 = fun.s3Connection()
    key = data['User'] + '/' + data['imType'] + '/red.png'
    response = fun.s3Upload(s3, data['Bucket'], 'red.png', key)

    return jsonify(response)