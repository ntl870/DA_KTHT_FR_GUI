import tkinter as tk
import cv2
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from PIL import ImageGrab
import base64
import numpy as np
import pyrebase
import os
import asyncio

import requests
import json
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()


def show_frame():
    _, frame = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #  Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # print(faces)
    # # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    return faces


show_frame()


async def upload(base64_string):
    url = "http://127.0.0.1:8000/identify"

    payload = json.dumps({
        "photo": base64_string
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload).status_code
    return response


def helloCallBack():
    success, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if(len(faces) != 1):
        messagebox.showinfo("Error", "Please take a photo of only you")
        return
    img_np = np.array(image)
    crop_img = img_np[faces[0][1]:faces[0][1] + faces[0]
                      [3], faces[0][0]:faces[0][0] + faces[0][2]]
    crop_img = np.array(crop_img)
    is_success, im_buf_arr = cv2.imencode(".jpg", crop_img)
    bytes_string = im_buf_arr.tobytes()
    encoded = base64.b64encode(bytes_string).decode("ascii")
    encoded = 'data:image/png;base64,{}'.format(encoded)
    cv2.imwrite('txt.jpg', crop_img)
    res_code = asyncio.run(upload(encoded))
    
    if(res_code == 200):
        messagebox.showinfo("Success", "Checked in successfully")
    else:
        messagebox.showinfo("Error", "Not Found")

    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)


# get image from camera cv2


B = Button(root, text="Hello", command=helloCallBack)

B.pack()
root.mainloop()
