
import streamlit as st
import cv2
import face_recognition as frg
import yaml 
from utils import recognize, build_dataset
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage 
from email.mime.text import MIMEText

# Path: code\app.py

st.set_page_config(layout="wide")
#Config
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']

st.sidebar.title("Settings")

#Create a menu bar
menu = ["Please Upload the Image of Suspect"]
choice = st.sidebar.selectbox("Input type",menu)
#Put slide to adjust tolerance
TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.5,0.01)
st.sidebar.info("chose tolerance according to the quality of your image .")

#Infomation section 
st.sidebar.title("Detected Criminal Information")
name_container = st.sidebar.empty()
id_container = st.sidebar.empty()

name_container.info('Criminal Name: Unnknown')
id_container.success('Criminal ID: Unknown')
if choice == "Please Upload the Image of Suspect":
    st.title("Surveillance app for the Gujarat Police")
    st.write(PICTURE_PROMPT)
    uploaded_images = st.file_uploader("Upload",type=['jpg','png','jpeg'],accept_multiple_files=True)
    if len(uploaded_images) != 0:
        #Read uploaded image with face_recognition
        for image in uploaded_images:
            image = frg.load_image_file(image)
            image, name, id = recognize(image,TOLERANCE) 
            name_container.info(f"Criminal Name: {name}")
            id_container.success(f"Criminal ID: {id}")
            st.image(image)
    else: 
        st.info("Please upload an image Of Criminal")


with st.sidebar.form(key='my_form'):
    submit_button = st.form_submit_button(label='REBUILD DATASET')
    if submit_button:
        with st.spinner("Rebuilding dataset..."):
            build_dataset()
        st.success("Dataset has been reset")



