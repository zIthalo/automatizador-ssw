import pyautogui
import time
import keyboard
import tkinter as tk
from datetime import datetime
from tkinter import simpledialog

data_atual = datetime.now().strftime("%d%m%Y")
dia = datetime.now().strftime("%d")

# Definição das funções de automação
def ag(): 
    pyautogui.click(x=224, y=375, clicks=3)
    ag_text = "AGENDAR ENTREGA".upper()
    pyautogui.write(ag_text)

def lc(): 
    pyautogui.click(x=216, y=456, clicks=3)
    lc_text = 'LOCAL DE ENTREGA'.upper()
    pyautogui.write(lc_text)
    pyautogui.press('enter')

def interior(): 
    pyautogui.click(x=205, y=314, clicks=3)
    pyautogui.write('093')
    time.sleep(.5)
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.press('enter')

def cem(): 
    pyautogui.click(x=205, y=314, clicks=3)
    pyautogui.write('100')
    time.sleep(.5)
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.press('enter')
def oito(): 
    pyautogui.click(x=205, y=314, clicks=3)
    pyautogui.write('008')
    time.sleep(.5)
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.press('enter')

# def log(): 
#     pyautogui.click(x=648, y=130)
#     pyautogui.write('')
#     pyautogui.press('enter')
#     pyautogui.write('')
#     pyautogui.press('')

def cub(): 
    pyautogui.click(x=549, y=328, clicks=2)

def ven(): 
    pyautogui.click(x=520, y=167)
    pyautogui.write('13631538000812')

def tec(): 
    pyautogui.click(x=520, y=167)
    pyautogui.write('08640510000992')

def mor(): 
    pyautogui.click(x=520, y=167)
    pyautogui.write('22161801000333')

def juando(): 
    pyautogui.click(x=520, y=167)
    pyautogui.write('79133583000340')

def sub(): 
    pyautogui.click(x=292, y=102, clicks=2)
    pyautogui.write('72090442000187')
    pyautogui.press('enter')
    pyautogui.write('BLU')
    pyautogui.press('enter')
    pyautogui.write(data_atual)
    pyautogui.press('enter')
    pyautogui.write(',01')
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.write(dia)
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.write('ARMAZEM')
    pyautogui.write('2')
    pyautogui.write('72090442000934')
    pyautogui.write('72090442000934')
    time.sleep(.5)
    pyautogui.press('enter')
    time.sleep(.5)
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.write('1')
    pyautogui.press('enter')
    pyautogui.write(data_atual)
    pyautogui.press('enter')
    pyautogui.write(',0001')
    pyautogui.press('enter')
    vl = pyautogui.prompt(text='Quantos volumes?', title='Entrada de Dados', default='1')
    pyautogui.write(vl)
    pyautogui.press('enter')
    pyautogui.write(',001')
    pyautogui.press('enter')
    pyautogui.write(',01')
    pyautogui.press('enter')
    sg = 'SEGUE '.upper()
    pl = ' PALLETS'.upper()
    pyautogui.write(sg + vl + pl)
    pyautogui.click(x=168, y=459)

def abrir_caixa_de_dialogo():
    root = tk.Tk()
    root.withdraw()
    comando = simpledialog.askstring("Entrada", "Digite um comando:")

    if comando in ["ag", "AG", "2"]:
        ag()
    elif comando in ["lc", "LC", "22"]:
        lc()
    elif comando in ["in", "IN", "1"]:
        interior()
    # elif comando in ["log", "LOG", "0"]:
    #     log()
    elif comando in ["cm", "CM", "11"]:
        cem()
    elif comando in ["cb", "CB", "3"]:
        cub()
    elif comando in ["vn", "VN", "5"]:
        ven()
    elif comando in ["ju", "JU", "55"]:
        juando()
    elif comando in ["tc", "TC", "4"]:
        tec()
    elif comando in ["mr", "MR", "44"]:
        mor()
    elif comando in ["sb", "SB", "6"]:
        sub()
    else:
        print("Comando não reconhecido!")

# Adiciona o atalho para pressionar Ctrl duas vezes
keyboard.add_hotkey('pause', abrir_caixa_de_dialogo)

print("Aguardando atalhos...")
keyboard.wait()  # Aguarda a execução do programa