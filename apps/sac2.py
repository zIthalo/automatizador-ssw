from datetime import datetime
import pyautogui
import time
import keyboard
import tkinter as tk
from tkinter import simpledialog

# Corrigindo a lógica de hora
hora_atual = datetime.now().hour

if 0 <= hora_atual < 12:
    saudacao = "Bom dia,"
elif 12 <= hora_atual < 18:
    saudacao = "Boa tarde,"
else:
    saudacao = "Boa noite,"

def endNaoLocalizado():
    pyautogui.write(saudacao, interval=0.05)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.write("Favor verificar.", interval=0.05)
    time.sleep(2)
    pyautogui.press("enter")
    pyautogui.write("Fomos na entrega da NF em assunto e o endereço não foi localizado.", interval=0.05)
    time.sleep(2)
    pyautogui.press("enter")
    pyautogui.write("Gentileza confirmar o endereço e caso o mesmo estiver divergente favor autorizar o custo de reentrega de 50% do valor do CT-e origem, nos encaminhar uma CC-e para endereço correto e informar um contato válido do cliente para alinhar nova tentativa de entrega.", interval=0.05)
    time.sleep(3)
    pyautogui.press("enter")
    pyautogui.write("Aguardamos breve retorno, para não prejudicar a entrega no cliente.", interval=0.05)
    time.sleep(2.5)

def reentrega():
    pyautogui.write(saudacao, interval=0.05)
    time.sleep(.5)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.write("Favor verificar.", interval=0.05)
    time.sleep(.5)
    pyautogui.press("enter")
    pyautogui.write("Fomos na entrega da NF em assunto e o destinatário estava ausente.", interval=0.05)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.write("Para prosseguir com a entrega, precisamos da autorização para custo de nova tentativa com valor de 50% do valor do CT-e origem e de um contato válido do destinatário para alinharmos nova tentativa.", interval=0.05)
    time.sleep(1.5)
    pyautogui.press("enter")
    pyautogui.write("Caso o endereço esteja divergente favor nos encaminhar uma CC-e para endereço correto também.", interval=0.05)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.write("Aguardamos breve retorno, para não prejudicar a entrega no cliente.", interval=0.05)

def abrir_caixa_de_dialogo():
    root = tk.Tk()
    root.withdraw()
    comando = simpledialog.askstring("Entrada", "Digite um comando:")

    if comando in ["1", "r"]:
        reentrega()
    elif comando in ["2", "nl"]:
        endNaoLocalizado()
    else:
        print("Comando não reconhecido.")

keyboard.add_hotkey("pause", abrir_caixa_de_dialogo)

print("Aguardando atalhos...")
keyboard.wait()