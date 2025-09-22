from datetime import datetime
import pyautogui
import time
import keyboard
import tkinter as tk
from tkinter import simpledialog
import pyperclip

#Msg Endereço não localizado

respostas = [
            #0
            "Favor verificar.\n\n",
            #1
            "\nFomos na entrega da NF em assunto e o endereço não foi localizado.",
            #2
            "\nGentileza confirmar o endereço e caso o mesmo estiver divergente favor autorizar o custo de reentrega de 50% do valor do CT-e origem, nos encaminhar uma CC-e para endereço correto e informar um contato válido do cliente para alinhar nova tentativa de entrega.",
            #3
            "\n\nAguardamos um breve retorno a fim de evitar impactos no prazo de entrega previsto para o cliente.\n", 
            #4
            "\nFomos na entrega da NF em assunto e o destinatário estava ausente.", 
            #5
            "\nPara seguir com uma nova tentativa de entrega, precisamos da autorização para custo de reentrega (50% do vlor do CT-e origem) e de um contato válido do cliente para alinharmos.", 
            #6
            "\nCaso o endereço esteja divergente favor nos encaminhar uma CC-e para o local correto também.",
            #7
            "\nFavor verificar e auxiliar.",
            #8
            "\nEstamos na entrega da NF em assunto aguardando descarregar.",
            #9
            "\nChegada: ",
            #10
            "\nSaída: "
]

respostasWpp = [
    #0
    "*Ithalo Willian.*\n",
    #1
    "\nTudo bem por aqui. E você?", 
    #2
    "\nVou verificar agora. Um momento.",
    #3
    "\nTudo bem?",
    #4
    "\nPreciso de um auxílio com esta NF:"
]

diversos = [
    #0 e-mail
    "sac.blu@arletetransportes.com.br",
    #1
    "\nPrecisamos de um breve retorno sobre este caso para finalizarmos esta tratativa."
]


# Corrigindo a lógica de hora
hora_atual = datetime.now().hour

if 0 <= hora_atual < 12:
    saudacao = "Bom dia,"
elif 12 <= hora_atual < 18:
    saudacao = "Boa tarde,"
else:
    saudacao = "Boa noite,"

#Funções

def endNaoLocalizado():
        
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyperclip.copy(respostas[0])
    pyautogui.hotkey("ctrl","v")
   
    pyperclip.copy(respostas[1])
    pyautogui.hotkey("ctrl","v")
   
    
    pyperclip.copy(respostas[2])
    pyautogui.hotkey("ctrl","v")
        
    pyperclip.copy(respostas[3])
    pyautogui.hotkey("ctrl","v")

def reentrega():

    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.press("enter")
    
    pyperclip.copy(respostas[0])
    pyautogui.hotkey("ctrl","v")
    
    pyperclip.copy(respostas[4])
    pyautogui.hotkey("ctrl","v")
   
    pyautogui.press("enter")
    pyperclip.copy(respostas[5])
    pyautogui.hotkey("ctrl","v")
   
    pyautogui.press("enter")
    pyperclip.copy(respostas[6])
    pyautogui.hotkey("ctrl","v")
    
    pyperclip.copy(respostas[3])
    pyautogui.hotkey("ctrl","v")

def estadia():

    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.press("enter")

    pyperclip.copy(respostas[7])
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    pyautogui.press("enter")

    pyperclip.copy(respostas[8])
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

    pyperclip.copy(respostas[9])
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

    pyperclip.copy(respostas[10])
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

def wpp():
    pyperclip.copy(respostasWpp[0])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[1])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[2])
    pyautogui.hotkey("ctrl", "v")

def wpp1():
    pyperclip.copy(respostasWpp[0])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[2])
    pyautogui.hotkey("ctrl", "v")
    
def wpp2():
    pyperclip.copy(respostasWpp[0])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[2])
    pyautogui.hotkey("ctrl", "v")

def wpp3():

    pyperclip.copy(respostasWpp[0])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(respostasWpp[3])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[4])
    pyautogui.hotkey("ctrl", "v")

def falarEmail():
    pyperclip.copy(diversos[0])
    pyautogui.hotkey("ctrl","v")

def cobrar():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyperclip.copy(diversos[1])
    pyautogui.hotkey("ctrl", "v")

def abrirCaixaDeDialogo():
    root = tk.Tk()
    root.withdraw()
    comando = simpledialog.askstring("Entrada", "Digite um comando:")

    if comando in ["3", "r"]:
        reentrega()
    elif comando in ["33", "nl"]:
        endNaoLocalizado()
    elif comando in ["4", "retorno"]:
        cobrar()
    elif comando in ["44", "estadia"]:
        estadia()
    elif comando in ["1", "wpp"]:
        wpp()
    elif comando in ["11", "wpp1"]:
        wpp1()
    elif comando in ["2", "wpp3"]:
        wpp3()
    elif comando in ["22", "email"]:
        falarEmail()
    else:
        print("Comando não reconhecido.")

keyboard.add_hotkey("pause", abrirCaixaDeDialogo)

print("Aguardando atalhos...")
keyboard.wait()