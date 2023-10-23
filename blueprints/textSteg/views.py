from main import app
from flask import request, jsonify
import functions as fun
import json

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
    key = data['User'] + '/' + data['imType'] + '/test.png'
    response = fun.s3Upload(s3, data['Bucket'], 'massive.png', key)

    return jsonify(response)

@app.route('/user/delete/image/', methods=['POST'])
def deleteImage():
    data = request.get_data()
    data = json.loads(data.decode())

    s3 = fun.s3Connection()
    response = fun.s3Delete(s3, data['Bucket'], data['Key'])

    return jsonify(response)

@app.route('/user/encode/image/', methods=['POST'])
def encodeImage():
    data = request.get_data()
    data = json.loads(data.decode())

    test = fun.encrypt(data['image'], data['message'])
    return(test)

@app.route('/user/decode/image/', methods=['POST'])
def decodeImage():
    data = request.get_data()
    data = json.loads(data.decode())

    test = fun.decrypt(data['image'])
    return(test)