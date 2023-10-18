from main import app
from flask import request, jsonify
import numpy as np
import functions as fun
import requests
import json
import cv2

@app.route('/textSteg/', methods=['POST'])
def placeHolder():
    data = request.get_data()
    data = json.loads(data.decode())
    return jsonify({'test': 'got'})