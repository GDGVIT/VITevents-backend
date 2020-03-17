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
app = flask.Flask(__name__)
app.config["DEBUG"] = False
# Comperator for Row segmentation
def compare(i,j):
    if j <= i+30 and j >= i-30:
        return True
    else:
        return False

# Function to Crop Image to required Proportions
def ImageExtractor(file):
    output = "done-"+file
    # Removing the column title
    frame = imread(file,0)

    li = []
    for i,dat in enumerate(frame[:,:]):
        count = 0
        for j,f in enumerate(dat):
            if (f > 223) and (f <= 255):
                count += 1
        if count/len(dat) >= 0.8:
            frame[i,:] =0
            li.append(i)
    done = 0
    for loc,i in enumerate(li):
        if loc == 0 : continue
        if i- li[loc-1] >= 20:
            done = i
            frame[i,:] = 100
            break
    x = list(frame.shape)
    done2 = x[0]
    for i in range(len(li),0,-1):
        if li[i-1] -li[i-2] >= 20:
            done2 = (li[i-1])
            break
    frame = imread(file,0)
    imwrite(output,frame)
    img = Image.open(output)
    img_left_area = (0, done, x[1], done2)
    img_left = img.crop(img_left_area)
    img_left.save(output)

    # Removing the Club Column
    li = []
    li2 = []
    frame = imread(output,0)
    frame = np.rot90(frame,k= 3)
    flag = False
    for i,dat in enumerate(frame[:,:]):
        count = 0

        for j,f in enumerate(dat):
            if (f > 230) and (f <= 255):
                count += 1
        if count/len(dat) > 0.7:
            frame[i,:] = 0
            flag = True
        else:
            if flag:
                li.append(i)
                flag = False

    for i in range(1,len(li)):
        if abs(li[i-1]-li[i]) > 50:
            li2.append(li[i])
            frame[li[i],:] = 150

    frame = np.rot90(frame,k= 1)
    x = list(frame.shape)
    imwrite(output,frame)


    

    #####
    frame = imread(output,0)
    li = []
    count = 0
    value = 0
    for i,dat in enumerate(frame[4,:]):

        if value != dat:
            value = dat
            count = 0
        else:
            count += 1
        if count >= 15:
            break
    flag = 0
    noted = 0
    for i,dat in enumerate(frame[4,:]):
        if dat == value:
            flag = 1
        else:
            if flag == 1 and (dat > 200 or dat < 100):
                noted  = i
                break
    frame[:,noted] = 0
    imwrite(output,frame)
    x = list(frame.shape)
    img = Image.open(output)
    img_left_area = (noted, 0, x[1], x[0])
    img_left = img.crop(img_left_area)
    img_left.save(output)

    # Removing the Contact Details
    frame = imread(output,0)
    frame = np.rot90(frame,k= 2)
    li = []
    count = 0
    value = 0
    for i,dat in enumerate(frame[4,:]):

        if value != dat:
            value = dat
            count = 0
        else:
            count += 1
        if count >= 15:
            break
    flag = 0
    noted = 0
    for i,dat in enumerate(frame[4,:]):
        if dat == value:
            flag = 1
        else:
            if flag == 1 and (dat > 200 or dat < 100):
                noted  = i
                break
    imwrite(output,frame)
    x = list(frame.shape)
    img = Image.open(output)
    img_left_area = (noted, 0, x[1], x[0])
    img_left = img.crop(img_left_area)
    img_left = img_left.rotate(180)
    img_left.save(output)

@app.route('/getTable', methods=['POST'])
def jsTableExtractor():
    try:
        content = request.get_data().decode('ASCII')
        if content is None:
            return(js.dumps({'status':'fail'}))
        load2 = []
        load = js.loads(content)
        load1 = (load['ParsedResults'][0]['TextOverlay']['Lines'])
        for loc,i in enumerate(load1):
            if re.match("Events on.*",i['LineText']):
                continue
            if re.match("Name.*",i['LineText']):
                continue
            if re.match("Chapter.*",i['LineText']):
                continue
            if re.match("Date.*",i['LineText']):
                continue
            if re.match("Venue.*",i['LineText']):
                continue
            if re.match(".*ime.*",i['LineText']):
                if re.match("Date.*",load1[loc-1]['LineText']):
                    continue
            if re.match("Contact.*",i['LineText']):
                continue
            if re.match("Person.*",i['LineText']):
                continue
            if re.match("Event.*",i['LineText']):
                continue
            for j in i['Words']:
                load2.append([j['WordText'],j['Left'],j['Top'],j['Height'],j['Width']])
        date_col = []
        for i in load2:
            if re.match('^[0-9]{2}-[0-9]{2}-[0-9]{4}$',i[0]):
                date_col.append(i)
        event = [[] for x in range(len(date_col))]
        time = [[] for x in range(len(date_col))]
        venue = [[] for x in range(len(date_col))]
        for loc,i in enumerate(date_col):
            for j in load2:
                if re.match('^[0-9]{2}-[0-9]{2}-[0-9]{4}$',j[0]): continue
                if re.match('^[0-9]{2}:[0-9]{2}$',j[0]) : continue
                if compare(i[2],j[2]):
                    if j[1] < i[1]:
                        event[loc].append(j)
                    else:
                        venue[loc].append(j)

        for loc,i in enumerate(date_col):
            for j in load2:
                if re.match('^[0-9]{2}-[0-9]{2}-[0-9]{4}$',j[0]): continue
                if re.match('^[0-9]{2}:[0-9]{2}$',j[0]) : 
                    if compare(i[2],j[2]):
                        time[loc].append(j)
        for i,data in enumerate(event):
            data.sort(key=lambda x: x[1])
            data.sort(key=lambda x: x[2])
            li = []
            for k in data:
                li.append(k[0])
            event[i] = " ".join(li)
        for i,data in enumerate(venue):
            data.sort(key=lambda x: x[1])
            data.sort(key=lambda x: x[2])
            li = []
            for k in data:
                li.append(k[0])    
            venue[i] = " ".join(li)

        for loc,i in enumerate(time):
            if len(i) > 0 : pass
            else:
                if re.match('^[0-9]{2}:[0-9]{2}',venue[loc]):
                    time[loc].append([venue[loc][:5]])
                    venue[loc] = venue[loc][5:]
        final = []
        for i in range(len(date_col)):
            try:
                final.append([event[i],time[i][0][0],date_col[i][0],venue[i]])
            except:
                pass
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