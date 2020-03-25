import flask
from flask import request
import requests
import json as js
import re
import base64
from random import random
import numpy as np
from io import BytesIO
import os
from PIL import Image

def RemoveColumnTitle(file,output):
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

def RemoveClubName(file,output):
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
def RemoveContactDetails(file,output):
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

def ImageExtractor(file):
    output = "done-"+file
    # Removing the column title
    RemoveColumnTitle(file,output)
    # Removing the Club Column
    RemoveClubName(file,output)
    # Removing the Contact Details
    RemoveContactDetails(file,output)
