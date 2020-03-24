# Required Libraries
import flask
from flask import request
import requests
import json as js
import re
import base64
from random import random
import numpy as np
from cv2 import imwrite,imread
from io import BytesIO
import os
from PIL import Image
from ImageEx import ImageExtractor
from tableExtract import tableEx
from utils import compare
app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.route('/getTable', methods=['POST'])
def jsTableExtractor():
    try:
        content = request.get_data().decode('ASCII')
        if content is None:
            return(js.dumps({'status':'fail'}))
        final = tableEx(content)
        return(js.dumps({'status':'success','events':final}))
    except:
        return(js.dumps({'status':'fail'}))
@app.errorhandler(404) 
def err404(e):
    return(js.dumps({'status':'fail'}))
@app.errorhandler(500) 
def err500(e):
    return(js.dumps({'status':'fail'}))

@app.route("/crop",methods=['POST'])
def cropImageAPIFuction():
    content = Image.open(request.files['img'])
    if content is None:
        return(js.dumps({'status':'fail'}))
    file = str(int(random()*(10**9))) + '.jpg'
    content.save(file)
    ImageExtractor(file)
    with open("done-"+file, "rb") as img_file:
         base64String = base64.b64encode(img_file.read())
    os.remove(file)
    os.remove("done-"+file)
    return(js.dumps({'status':'sucess','img':base64String.decode('ASCII')}))

@app.route("/cropb64",methods=['POST'])
def cropBase64ImageAPIFunction():
    content = request.get_data()
    if content is None:
        return(js.dumps({'status':'fail'}))
    file = str(int(random()*(10**9))) + '-.jpg'
    fh = open(file,'wb')
    fh.write(base64.decodebytes(content))
    fh.close()
    ImageExtractor(file) 
    with open("done-"+file, "rb") as img_file:
         base64String = base64.b64encode(img_file.read())
    os.remove(file)
    os.remove("done-"+file)
    return(js.dumps({'status':'sucess','img':base64String.decode('ASCII')}))
if __name__ == '__main__':
    app.run(debug=True)