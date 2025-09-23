from datetime import datetime
import pyautogui
import keyboard
import pyperclip
import tkinter as tk

janela = tk.Tk()
janela.title("Meu Programa Python")
janela.geometry("300x200")  # largura x altura

# Botão para fechar
botao_fechar = tk.Button(janela, text="Fechar", command=janela.destroy)
botao_fechar.pack(pady=20)

janela.mainloop()


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
    "*Ithalo Willian:*\n\n",
    #1
    "\n\nTudo bem por aqui. E você?", 
    #2
    "\n\nVou verificar agora, só um momento.",
    #3
    "\n\nTudo bem?",
    #4
    "\n\nPreciso de um auxílio com esta NF: ",
    #5
    "\n\nSegue e-mail referente a NF: "
]

mudouse = "\nFomos na entrega da NF em assunto e nos informaram que o cliente mudou-se.\nGentileza verificar e nos encaminhar uma CC-e para o endereço correto e autorizar o custo de reentrega de 50% do valor do CT-e origem.\nAguardamos breve retorno afim de não prejudicar o prazo de entrega do cliente."


diversos = [
    #0 e-mail
    "sac.blu@arletetransportes.com.br",
    #1
    "\n\nPrecisamos de um breve retorno sobre este caso para finalizarmos esta tratativa.",
    #2
    "\nEsta mercadoria está em rota de entrega hoje, deve ser finalizada em horário comercial até as 18h.",
    #3
    "\n\nTemos retorno sobre este caso?"
]



# Corrigindo a lógica de hora
hora_atual = datetime.now().hour

if 0 <= hora_atual < 12:
    saudacao = "Bom dia."
elif 12 <= hora_atual < 18:
    saudacao = "Boa tarde."
else:
    saudacao = "Boa noite."

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
    
def wppVouVerificar():
    pyperclip.copy(respostasWpp[0])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[2])
    pyautogui.hotkey("ctrl", "v")

def wppAuxilioNf():

    pyperclip.copy(respostasWpp[0])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(respostasWpp[3])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[4])
    pyautogui.hotkey("ctrl", "v")

def wppSegueEmail():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")
    pyperclip.copy(respostasWpp[5])
    pyautogui.hotkey("ctrl","v")
def wppMercEmRota():
    pyperclip.copy(diversos[2])
    pyautogui.hotkey("ctrl","v")

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

def cobrar2():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")
    pyperclip.copy(diversos[3])
    pyautogui.hotkey("ctrl","v")

def mudouSe():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")
    pyperclip.copy(mudouse)
    pyautogui.hotkey("ctrl","v")
comando_digitado = ""

def verificar_comando(e):
    global comando_digitado
    tecla = e.name

def apagar_comando(tamanho):
    for _ in range(tamanho):
        keyboard.send('backspace')

def verificar_comando(e):
    global comando_digitado
    tecla = e.name

    if len(tecla) == 1 or tecla in ["space", "enter", "slash"]:
        if tecla == "space":
            comando_digitado += " "
        elif tecla == "enter":
            comando_digitado += "\n"
        elif tecla == "slash":
            comando_digitado += "/"
        else:
            comando_digitado += tecla

        # Verifica comandos
        if "//1" in comando_digitado:
            apagar_comando(3)
            wpp()
            comando_digitado = ""
        elif "//2" in comando_digitado:
            apagar_comando(3)
            wppVouVerificar()
            comando_digitado = ""
        elif "//3" in comando_digitado:
            apagar_comando(3)
            wppAuxilioNf()
            comando_digitado = ""
        
        elif "//4" in comando_digitado:
            apagar_comando(3)
            reentrega()

            comando_digitado = ""
        elif "//5" in comando_digitado:
            apagar_comando(3)
            endNaoLocalizado()
            comando_digitado = ""
        
        elif "//6" in comando_digitado:
            apagar_comando(3)
            mudouSe()
            comando_digitado = ""
        elif "//7" in comando_digitado:
            apagar_comando(3)
            cobrar()
            comando_digitado = ""
        elif "//8" in comando_digitado:
            apagar_comando(3)
            cobrar2()
            comando_digitado = ""
        elif "//9" in comando_digitado:
            apagar_comando(3)
            estadia()
            comando_digitado = ""
        elif "//e" in comando_digitado:
            apagar_comando(3)
            falarEmail()
            comando_digitado = ""
        elif "//r" in comando_digitado:
            apagar_comando(3)
            wppMercEmRota()
            comando_digitado = ""
        elif "//sg" in comando_digitado:
            apagar_comando(4)
            wppSegueEmail()
            comando_digitado = ""
        elif len(comando_digitado) > 10:
            comando_digitado = ""

keyboard.on_press(verificar_comando)

print("Monitorando comandos digitados como //1, //2, etc...")
keyboard.wait()

