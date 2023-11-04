
import streamlit as st
import cv2
import face_recognition as frg
import yaml 
from utils import recognize, build_dataset
import pandas as pd 
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
from io import BytesIO

def getTime():
  IST = pytz.timezone('Asia/Kolkata')
  timeNow = datetime.now(IST)
  return timeNow
  
def send_alert(loc,name,id,img) : 
        time_moment = getTime()  
        bot = telepot.Bot('6645598193:AAGE14mNJMgrpMMg1oYNs5Q9HI-Xo-e2j8Q') 
        bot.sendMessage(5117088003, f"Criminal Alert : Criminal with name : {name} and ID : {id} is Detected !!\nLOCATION: {loc}\nTIME: {time_moment} ")
        img_io = BytesIO(img)
        bot.sendPhoto(5117088003, photo=('img.jpg',img_io ))
        send_alert = 1

def cam_view(loc ,cam) : 
    cam = cv2.VideoCapture(cam) 
    show_view = st.image([]) 
    id_list = [] 
    
    while True:
        ret , frame = cam.read() 
        if not ret:
            st.error("Failed to capture frame from CCTV")
            st.info("Please turn off the other app that is using the CCTV Or restart app")
            st.stop()
        image, name, id = recognize(frame,TOLERANCE)
        image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)

        name_container_1.info(f"Criminal Name: {name}")
        id_container_1.success(f"Criminal ID: {id}")
        show_view.image(image) 

        if name!= "Unknown" and id not in id_list :
            id_list.append(id)  
            image_bytes = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))[1].tobytes()
            send_alert(loc,name,id,image_bytes)


st.set_page_config(layout="wide")
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']

st.title("Surveillance app for the Gujarat Police")
st.write(WEBCAM_PROMPT)
st.sidebar.title("Settings")

menu = ["Please Select the Area for Servellance"]
choice = st.sidebar.selectbox("Please Select Area For Servellence : ",menu)

TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.5,0.01)
st.sidebar.warning("chose tolerance according to the quality of CCTV camera.")


st.sidebar.title("Criminal Information at Giver Location : ") 
name_container_1= st.sidebar.empty()
id_container_1 = st.sidebar.empty()
name_container_1.info('Criminal Name: Unnknown')
id_container_1.success('Criminal ID: Unknown')

   
if  choice == "Please Select the Area for Servellance":

    city_mapping = {
    'GEC RAJKOT': 0,
    'Airport': 1,
    'Rajkot Police Station': 2,
    'CM - Office' : 3 }

    selected_city = st.selectbox('Please select Area for Servellance:', list(city_mapping.keys()))

    if selected_city == 'GEC RAJKOT' :
        start = st.button('show Live Footage') 
        if start : 
            cam_view(selected_city,0)
        
    elif selected_city == 'Airport' :
        start = st.button('show Live Footage') 
        if start : 
            cam_view(selected_city,0)

    elif selected_city == 'Police Station' :
        start = st.button('show Live Footage') 
        if start : 
            cam_view(selected_city,0)

    elif selected_city == 'CM - Office' : 
        start = st.button('show Live Footage') 
        if start : 
            cam_view(selected_city,0)

    






        # if name!= "Unknown" and id not in id_list :
        #     id_list.append(id)  
        #     mail_authority(id,name, image) 



with st.sidebar.form(key='my_form'):
    submit_button = st.form_submit_button(label='REBUILD DATASET')
    if submit_button:
        with st.spinner("Rebuilding dataset..."):
            build_dataset()
        st.success("Dataset has been reset")



