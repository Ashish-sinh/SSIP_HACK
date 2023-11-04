from keras.models import load_model
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pickle
import cv2
import telepot
from datetime import datetime
import pytz
from PIL import Image
from PIL import ImageEnhance
import os
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from mtcnn.mtcnn import MTCNN 
import streamlit as st 


def getTime():
  IST = pytz.timezone('Asia/Kolkata')
  timeNow = datetime.now(IST)
  return timeNow

def imgenhance():
  image1 = Image.open('save_imagessavedImage.jpg')
  curr_bri = ImageEnhance.Sharpness(image1)
  new_bri = 1.3
  img_brightened = curr_bri.enhance(new_bri)
  im1 = img_brightened.save("save_image/bright.jpg")

  image2 = Image.open('final_image/bright.jpg')
  curr_col = ImageEnhance.Color(image2)
  new_col = 1.5
  img_col = curr_col.enhance(new_col)
  im2 = img_col.save("final_image/finalImage.jpg")

def draw_faces(filename, result_list):

    data = pyplot.imread(filename)
    # plot each face as a subplot
    for i in range(len(result_list)):
        # get coordinates
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        # define subplot
        pyplot.subplot(1, len(result_list), i+1)
        pyplot.axis('off')
        # plot face
        pyplot.imshow(data[y1:y2, x1:x2])

    pyplot.savefig("detected_suspect/faces.png")
    pyplot.show()

def detectViolence(location,cam, limit=None):
        trueCount = 0
        imageSaved = 0
        filename = 'savedImage.jpg'
        my_image = 'finalImage.jpg'
        face_image = 'faces.png'
        sendAlert = 0
        location = location
        show_image = st.image([]) 

        print("Loading model ...")
        model = load_model('my_model_for_violance.h5')
        Q = deque(maxlen=128)
        vs = cv2.VideoCapture(cam)

        writer = None
        (W, H) = (None, None)
        count = 0
        while True:
            (grabbed, frame) = vs.read()

            if not grabbed:
                break

            if W is None or H is None:
                (H, W) = frame.shape[:2]
            output = frame.copy()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (128, 128)).astype("float32")
            frame = frame.reshape(128, 128, 3) / 255

            preds = model.predict(np.expand_dims(frame, axis=0))[0]
            Q.append(preds)

            results = np.array(Q).mean(axis=0)
            i = (preds > 0.50)[0]
            label = i

            text_color = (0, 255, 0) # default : green

            if label: # Violence prob
                text_color = (0, 0, 255) # red
                trueCount = trueCount + 1

            else:
                text_color = (0, 255, 0)

            text = "Violence: {}".format(label)
            FONT = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(output, text, (35, 50), FONT,1.25, text_color, 3)

            if writer is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter("saved_video/recordedVideo.avi", fourcc, 30,(W, H), True)

            # write the output frame to disk
            writer.write(output)

            # show the output image
            show_image.image(output)

            if(trueCount == 40):
              if(imageSaved == 0):
                if(label):
                  cv2.imwrite(filename, output)
                  imageSaved = 1

              if(sendAlert == 0):
                timeMoment = getTime()
                imgenhance()
                pixels = pyplot.imread(my_image)

                detector = MTCNN()
                faces = detector.detect_faces(pixels)
                draw_faces(my_image, faces)

                bot = telepot.Bot('6645598193:AAGE14mNJMgrpMMg1oYNs5Q9HI-Xo-e2j8Q') ## GET YOUR OWN TELEGRAM GROUP ID AND BOT ID
                bot.sendMessage(5117088003, f"VIOLENCE DETECTED AT : !! \nLOCATION: {location} \nTIME: {timeMoment}")
                bot.sendPhoto(5117088003, photo=open('finalImage.jpg', 'rb'))
                bot.sendMessage(5117088003, "FACES OBTAINED")
                bot.sendPhoto(5117088003, photo=open('faces.png', 'rb'))



st.title('Violance Detection On Given Location')
task = st.sidebar.selectbox('select' ,['CCTV Camera','upload Videos To Detect Violance']) 

if task == 'CCTV Camera' :
  
  selected_city = st.selectbox('Please select a city:',['GEC RAJKOT','Airport', 'Rajkot Police Station','CM - Office' ] )

  if selected_city == 'GEC RAJKOT' :
        start = st.button('show Live Footage') 
        if start : 
            detectViolence(selected_city,cam=0)
          
  elif selected_city == 'Airport' :
          start = st.button('show Live Footage') 
          if start : 
              detectViolence(selected_city,cam=0)

  elif selected_city == 'Police Station' :
    start = st.button('show Live Footage')
    if start :
      detectViolence(selected_city,cam=0)

  elif selected_city == 'CM - Office': 
    start = st.button('show Live Footage')
    if start :
          detectViolence(selected_city,cam=0)

if task == 'upload Videos To Detect Violance' : 

  path = st.text_input('enter file name over the test folder')
  path = 'test_video/'+str(path)

  detectViolence(location='test_video', cam= path )

