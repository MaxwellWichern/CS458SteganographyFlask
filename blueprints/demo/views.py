from main import app
from flask import request


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