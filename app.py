import re
from tkinter.tix import IMAGE
from flask import Flask, render_template, request, jsonify
from PIL import Image
import os
import io
import sys
import numpy as np
import cv2
import base64
from detector_rev2 import detect_number
from urllib import response
import requests
import json

app = Flask(__name__)

############################################## THE REAL DEAL ###############################################


@app.route('/detectObject', methods=['POST'])
def mask_image():
    # print(request.files , file=sys.stderr)
    file = request.files['image']  # byte file
    file.save(os.path.join('/', 'demo.jpg'))
    ######### Do preprocessing here ################
    # img[img > 150] = 0
    # any random stuff do here
    ################################################

    url = "http://127.0.0.1:5019"
    with open('/demo.jpg', 'rb') as f:
        try:
            r = requests.post(url, files={'image': f})
        except requests.exceptions.ConnectionError:
            response.status_code = 'Connection Refused'

    res = r.json()
    return res

##################################################### THE REAL DEAL HAPPENS ABOVE ######################################


@app.route('/')
def home():
    return render_template('./index.html')


@app.after_request
def after_request(response):
    print("log: setting cors", file=sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5001)
