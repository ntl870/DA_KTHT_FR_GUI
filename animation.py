import tkinter as tk
from PIL import Image
import threading
import time


file="loader.gif"
info = Image.open(file)
frames = info.n_frames  # gives total number of frames that gif contains
# creating list of PhotoImage objects for each frames
# im = [tk.PhotoImage(file=file,format=f"gif -index {i}"w) for i in range(frames)]
im= None
anim = None
def animation(count,loadingWindow, gif_label):
    global anim
    global im
    im2 = im[count]

    gif_label.configure(image=im2)
    count += 1
    if count == frames:
        count = 0
    anim = loadingWindow.after(50,lambda :animation(count,loadingWindow,gif_label))
    
def executeLoadingWindow():
    count = 0
    global im
    loadingWindow = tk.Tk()
    im = [tk.PhotoImage(file=file,format=f"gif -index {i}") for i in range(frames)]
    gif_label = tk.Label(loadingWindow,image="")
    
    gif_label.pack()
    animation(count,loadingWindow,gif_label)

    loadingWindow.mainloop()
    
def sleep():
    time.sleep(3)
    
t2 = threading.Thread(target=executeLoadingWindow())    
t1 = threading.Thread(target=sleep())
t2.join()
t1.join()
print('done')