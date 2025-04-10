import pyautogui
import time
import keyboard


keyboard.wait('alt+A')

time.sleep(1.2)

pyautogui.click(x=833, y=1052)
time.sleep(1.2)
pyautogui.click(x=24, y=562)
time.sleep(.5)
pyautogui.write("*** AGENDAR ENTREGA ***")
time.sleep(1)

 
keyboard.wait('alt+Q')

pyautogui.click(x=833,y=1052)
time.sleep(1.2)
pyautogui.click(x=25,y=651)
time.sleep(1.2)
pyautogui.write('LOCAL DE ENTREGA')