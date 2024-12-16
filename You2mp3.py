# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:33:59 2024

@author: vtteam
"""

# TKinter playgroud

#%%
import tkinter as tk     
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

def warning_windows(text):
    window = tk.Tk()
    window.title('通知')
    window.geometry("1000x400+800+200")
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = tk.Label(window, text = text + '\n' + now_time,
                     bg = '#EEBB00',         #  背景顏色
                     font = ('Arial', 15),   # 字型與大小
                     width = 50, height = 30)  # 顯示文字
    label.pack()
    window.mainloop()

#%%
def save(): 
    files = [('All Files', '*.*'),  
             ('Python Files', '*.py'), 
             ('Text Document', '*.txt'),
             ('mp3 file', '*.mp3')] 
    file = filedialog.asksaveasfile(filetypes = files, defaultextension = files) 


window = tk.Tk()
window.title('File Explorer')
window.geometry("500x500")
window.config(background = "white")

btn = tk.Button(window, text = 'Save', command = lambda : save()) 
btn.pack(side = TOP, pady = 20) 
  
window.mainloop() 



#%%

































