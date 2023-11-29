from main import app
from flask import request, jsonify
import functions as fun
import json
import tempfile
import requests

@app.route('/user/all/images/', methods=['POST'])
def getImages():
    data = request.form

    s3 = fun.s3Connection()
    userImages = fun.genUsersLinks(s3, 'stegosaurus', data['User'], data['imType'])['Contents']
    urls = []
    for item in userImages:
        print(item['Key'])
        URL = fun.s3URL(s3, 'stegosaurus', item['Key'])
        urls.append(URL)

    # print(len(urls))
    # print(urls)
    return jsonify({'Links': urls})

@app.route('/user/upload/image/', methods=['POST'])
def uploadImage():
    data = request.form

    s3 = fun.s3Connection()
    key = data['User'] + '/' + data['imType'] + '/red.png'
    response = fun.s3Upload(s3, data['Bucket'], 'red.png', key)

    return jsonify(response)

@app.route('/user/delete/image/', methods=['POST'])
def deleteImage():
    data = request.form

    s3 = fun.s3Connection()
    response = fun.s3Delete(s3, data['Bucket'], data['Key'])

    return jsonify(response)

@app.route('/user/delete/user/', methods=['POST'])
def deleteUser():
    data = request.form

    s3 = fun.s3Connection()
    bucket = s3.Bucket(data['Bucket'])
    bucket.objects.filter(Prefix=data['Key']).delete()

    return jsonify({'Deleted': data['Key']})

@app.route('/user/encode/image/', methods=['POST'])
def encodeImage():

    switch = False
    data = request.form
    try:
        file = request.files['file']
    except:
        file = data['preview']
        switch = True

    finally:
        with tempfile.TemporaryDirectory() as tmpDir:
            fileName = fun.timeStamp() + '.png'
            filePath = tmpDir + '/' + fileName
            if not switch:
                file.save(filePath)
            else:
                response = requests.get(file)
                with open(filePath, 'wb') as f:
                    f.write(response.content)
                del response

            s3 = fun.s3Connection()
            key = data['User'] + '/OrigImg/' + fileName
            uploadOrg = fun.s3Upload(s3, 'stegosaurus', filePath, key)

            encodeResponse = fun.encrypt(filePath, data['Hidden'], tmpDir)

            key = data['User'] + '/EncryptedImg/' + encodeResponse['fileName']
            uploadEnc = fun.s3Upload(s3, 'stegosaurus', tmpDir + '/' + encodeResponse['fileName'], key)
            imgLink = fun.s3URL(s3, 'stegosaurus', key)

    return jsonify({'imgLink': imgLink})

@app.route('/user/decode/image/', methods=['POST'])
def decodeImage():
    
    switch = False
    data = request.form
    print(data)
    try:
        file = request.files['file']
    except:
        file = data['preview']
        switch = True

    finally:
        with tempfile.TemporaryDirectory() as tmpDir:
            filePath = tmpDir + '/' + fun.timeStamp() + '.png'
            if not switch:
                file.save(filePath)
            else:
                response = requests.get(file)
                with open(filePath, 'wb') as f:
                    f.write(response.content)
                del response

            decodeResponse = fun.decrypt(filePath)
            # print(decodeResponse)

    return(decodeResponse)