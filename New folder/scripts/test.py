import os
import sys
import json
import requests
import base64
import random
import csv
import ctypes
import win32con
import win32api
import win32gui
import win32com.client 
import logzero
import pandas as pd
import math
import time, pyautogui
import PySimpleGUI as sg
import multiprocessing
import pandas as pd
from calendar import isleap
from datetime import datetime
from operator import itemgetter
from logzero import logger
from time import sleep
from openpyxl import load_workbook
from time import sleep, time
from pywinauto import Desktop, Application, Desktop
from win32gui import GetWindowText, GetForegroundWindow


def refresh_smart():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    smartview=f'{ROOT_DIR}\\finalclose\\excels\\translationAPAC.xlsx'
    #ejemplo = f'{ROOT_DIR}\\roba_\\ejemplo.html'
    print(smartview)
    app = Application(backend="uia").start(rf"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE {smartview}")
    """  pid= app.process_id()
    app.connect(pid)
    app.Maximize()
    app.set_focus() """
    sleep(120)
    #app.Minimize()
    sleep(5)
    #app.restore()
    #sleep(5)
    #app.Maximize()
    #sleep(10)
    shell = win32com.client.Dispatch('WScript.Shell')
    windows = Desktop(backend="uia").windows()
    w= [w for w in windows]
    exce = None
    for i in w:
        if "Excel" in i.window_text():
            exce = i
    if exce != None:
        exce.maximize()
        exce.set_focus()
    win= GetForegroundWindow()
    win32gui.SetForegroundWindow(win)
    shell.SendKeys("%S")
    sleep(1)
    shell.SendKeys("D")
    sleep(1)
    shell.SendKeys("R")
    sleep(1)
    shell.SendKeys("R")
    sleep(15)
    shell.SendKeys('bot_aae_is_r_dev\tVdj&Ty3?pFq;Zy\t\t')
    sleep(2)
    shell.SendKeys('{ENTER}')  # Enter key
    sleep(100)
    w= [w for w in windows]
    exce = None
    for i in w:
        if "Excel" in i.window_text():
            exce = i
    if exce != None:
        exce.maximize()
        exce.set_focus()
    win= GetForegroundWindow()
    win32gui.SetForegroundWindow(win)
    #shell.SendKeys('{ESCAPE}')
    #sleep(1)
    shell.SendKeys('%f')
    sleep(1)
    shell.SendKeys('A')
    sleep(1)
    shell.SendKeys('Y')
    sleep(1)
    shell.SendKeys('3')
    sleep(1)
    shell.SendKeys(f'APAC_validation')
    sleep(1)
    shell.SendKeys('{ENTER}')
    sleep(1)
    shell.SendKeys('{LEFT}')
    sleep(1)
    shell.SendKeys('{ENTER}')
    sleep(1)
    shell.SendKeys('{ENTER}')
    sleep(1)
    shell.SendKeys('%{F4}')




def validation():
    notif = ""
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_excel (f'{ROOT_DIR}\\finalclose\\excels\\APAC_validation.xlsx')
    cold = df.iloc[ 2:9,3]
    colg= df.iloc[ 13:19,6]
    print("Cold")
    for i in cold:
        print(i)
        try:
            x=float(i)
            if i > 1.0:
                return "Error: some values are grater than 1 dollar"
        except:
            return "Error at time to convert"
    print("Colg") 
    for i in colg:
        print(i)
        try:
            x=float(i)
            if i > 1.0:
                return "Error: some values are grater than 1 dollar"
        except:
            return "Error at time to convert" 