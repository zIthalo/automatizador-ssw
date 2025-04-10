import pyautogui
import time
import keyboard
import tkinter as tk
from tkinter import simpledialog



def realizar_primeira_tarefa():
    pyautogui.click(x=24, y=562, clicks=3)
    time.sleep(.5)
    pyautogui.write("***AGENDAR ENTREGA***")
    time.sleep(1)

def realizar_segunda_tarefa():
    pyautogui.click(x=25, y=651, clicks=3)
    time.sleep(.5)
    pyautogui.write('***LOCAL DE ENTREGA***')
    time.sleep(1)

def realizar_terceira_tarefa():
    pyautogui.click(x=25, y=651, clicks=3)
    time.sleep(.5)
    pyautogui.write('93')
    time.sleep(1)
    
# keyboard.add_hotkey('alt+1', realizar_primeira_tarefa)
# keyboard.add_hotkey('alt+2', realizar_segunda_tarefa)
# keyboard.add_hotkey('alt+3', realizar_terceira_tarefa)

def abrir_caixa_de_dialogo():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    comando = simpledialog.askstring("Entrada", "Digite um comando:")

    if comando == "ag":
        realizar_primeira_tarefa()
    elif comando == "lc":
        realizar_segunda_tarefa()
    elif comando == "in":
        realizar_terceira_tarefa()
    else:
        print("Comando não reconhecido!")

# Associa o comando 'alt+D' para abrir a caixa de diálogo
keyboard.add_hotkey('alt+-', abrir_caixa_de_dialogo)



print("Aguardando atalhos: ")
keyboard.wait()  # Aguarda o programa continuar rodando