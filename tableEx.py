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
from utils import compare

def tableEx(content):
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
