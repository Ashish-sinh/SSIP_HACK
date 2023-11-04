
import pandas as pd 
import cv2
import torch
import numpy as np
import streamlit as st
from PIL import Image
from collections import deque
import argparse
import pickle
import telepot
from datetime import datetime
import pytz
import PIL as Image 
from io import BytesIO


import telepot

def getTime():
  IST = pytz.timezone('Asia/Kolkata')
  timeNow = datetime.now(IST)
  return timeNow

def send_alert(loc,img) : 
        time_moment = getTime()  # Implement your get_time function
        bot = telepot.Bot('6645598193:AAGE14mNJMgrpMMg1oYNs5Q9HI-Xo-e2j8Q')  # Replace with your Telegram bot token
        bot.sendMessage(5117088003, f"Loitring ALERT!!\nLOCATION: {loc}\nTIME: {time_moment} ")
        img_io = BytesIO(img)
        bot.sendPhoto(5117088003, photo=('img.jpg',img_io ))
        send_alert = 1


CLASSES = [ 'person' ]


st.set_page_config(
    page_title="Person Loitering Detection and Aleart",
    page_icon='') 


st.title('Person Loitering Detection and Aleart')

@st.cache_resource(max_entries=2)
def get_yolo5(model_type='s'):
  
    return torch.hub.load('ultralytics/yolov5', 
                          'yolov5{}'.format(model_type), 
                          pretrained=True )

@st.cache_resource(max_entries=10)
def get_preds(img : np.ndarray) -> np.ndarray:
  
    return model([img]).xyxy[0].numpy() 
 
def display_cctv(loc,n) : 

    cam = cv2.VideoCapture(n)
    show_frame = st.image([])
    show_text = st.markdown("")
    person_detection = False 
    alert = 0  

    while True : 
        ret , frame = cam.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result =get_preds(img)
        result = result[np.isin(result[:,-1],target_class_ids)]

        if len(result) > 0 : 
            if (alert >=20 or alert ==0):
                show_text.empty()  
                show_text = st.markdown("<h1 style='color: red;'>Person is detected </h3>", unsafe_allow_html=True)
                image_bytes = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))[1].tobytes()
                send_alert(loc,image_bytes) 
                alert+=1
            else :
                show_text.empty()  
                show_text = st.markdown("<h1 style='color: red;'>Person is detected </h3>", unsafe_allow_html=True)

             

        else : 
            show_text.empty()
            show_text = st.markdown("<h1 style='color: green;'> No person in the frame</h3>", unsafe_allow_html=True) 

        for bbox_data in result:
            xmin, ymin, xmax, ymax, _, label = bbox_data
            p0, p1, label = (int(xmin), int(ymin)), (int(xmax), int(ymax)), int(label)
            img = cv2.rectangle(img, 
                                    p0, p1, 
                                    (255,0,0), 3) 

                
        show_frame.image(img) 


model_type = 's'

with st.spinner('Loading the CCTV Data...'):
    model = get_yolo5(model_type)
st.success('Loading CCTV Data.. Completed !')

prediction_mode = 'Web camera' 

target_class_ids = [0]

if prediction_mode == 'Web camera':

    city_mapping = {
    'GEC RAJKOT': 0,
    'Airport': 1,
    'Rajkot Police Station': 2,
    'CM - Office' : 3 }

    selected_city = st.selectbox('Please select a city:', list(city_mapping.keys()))

    if selected_city == 'GEC RAJKOT' :
        start = st.button('show Live Footage') 
        if start : 
            display_cctv(loc=selected_city,n=0)
        
    elif selected_city == 'Airport' :
        start = st.button('show Live Footage') 
        if start : 
            display_cctv(loc=selected_city,n=0)

    elif selected_city == 'Police Station' :
        start = st.button('show Live Footage') 
        if start : 
            display_cctv(loc=selected_city,n=0)

    elif selected_city == 'CM - Office' : 
        start = st.button('show Live Footage') 
        if start : 
            display_cctv(loc=selected_city,n=0)

    