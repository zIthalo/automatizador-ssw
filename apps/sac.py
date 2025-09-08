import pyautogui
import datetime
import time
import pyautogui
import time
import keyboard
import tkinter as tk
from datetime import datetime
from tkinter import simpledialog

time.sleep(5)

# Obtém a hora atual
hora_atual = datetime.now().hour

# Define a saudação com base na hora
if 0 <= hora_atual < 12:
    saudacao = "Bom dia,"
elif 12 <= hora_atual < 18:
    saudacao = "Boa tarde,"
else:
    saudacao = "Boa noite,"

def endNaoLocalizado():
    pyautogui.write(saudacao)
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.write("Favor verificar.")
    time.sleep(2)
    pyautogui.press("enter")
    pyautogui.write("Fomos na entrega da NF em assunto e o endereço não foi localizado.")
    time.sleep(2)
    pyautogui.press("enter")
    pyautogui.write("Gentileza confirmar o endereço e caso o mesmo estiver divergente favor autorizar o custo de reentrega de 50% do valor do CT-e origem, nos encaminhar uma CC-e para endereço correto e informar um contato válido do cliente para alinhar nova tentativa de entrega.")
    time.sleep(3)
    pyautogui.press("enter")
    pyautogui.write("Aguardamos breve retorno, para não prejudicar a entrega no cliente.")
    time.sleep(2.5)


def reentrega():
    pyautogui.write(saudacao)
    time.sleep(.5)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.write("Favor verificar.")
    time.sleep(.5)
    pyautogui.press("enter")
    pyautogui.write("Fomos na entrega da NF em assunto e o destinatário estava ausente.")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.write("Para prosseguir com a entrega, precisamos da autorização para custo de nova tentativa com valor de 50% do valor do CT-e origem e de um contato válido do destinatário para alinharmos nova tentativa.") 
    time.sleep(1.5)
    pyautogui.press("enter")
    pyautogui.write("Caso o endereço esteja divergente favor nos encaminhar uma CC-e para endereço correto também.")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.write("Aguardamos breve retorno, para não prejudicar a entrega no cliente.")

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
    
# Adiciona o atalho para pressionar pressione Pause Break
keyboard.add_hotkey("pause", abrir_caixa_de_dialogo)

print("Aguardando atalhos...")
keyboard.wait()  # Aguarda a execução do programa

