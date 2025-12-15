from datetime import datetime
import pyautogui
import keyboard
import pyperclip
import tkinter as tk


def mostrar_comandos():
    comandos = [
        "Digite //0 para executar a função saudação breve\n",
        "Digite //1 para executar a função de saudação completa no wpp;\n",
        "Digite //2 para executar a função saudação2;\n",
        "Digite //3 para executar a função solicitar auxilio com uma nf;\n",
        "Digite //4 para executar a função de email de reentrega\n;",
        "Digite //5 para executar a função de email de endereço não localizado\n;",
        "Digite //6 para executar a função de destinatário mudou-se;\n",
        "Digite //7 para executar a função cobrar retorno;\n",
        "Digite //8 para executar a função cobrar retorno 2;\n",
        "Digite //9 para executar a função informar estadia;\n",
        "Digite //e para executar a função informar seu e-mail;",
        "Digite //r para executar a função informar que a mercadoria está em rota de entrega hoje;\n",
        "Digite //sg para executar a função segue e-mail enviado;\n",
        "Digite //ag para executar a função informar agendamento\n",
        "Digite //ar para executar a função informar agendamento Risso\n",
        "Digite //ca para executar a função cobrar agendamento para amanhã\n",
        "Digite //p para executar a função teria o PDF ou n° da NF?\n"
    ]

    janela = tk.Tk()
    janela.title("Comandos disponíveis")
    janela.geometry("400x400")

    texto = tk.Text(janela, wrap="word", font=("Arial", 10))
    texto.pack(expand=True, fill="both", padx=10, pady=10)

    for linha in comandos:
        texto.insert("end", linha + "\n")

    botao_fechar = tk.Button(janela, text="Fechar", command=janela.destroy)
    botao_fechar.pack(pady=10)

    janela.mainloop()


#Msg Endereço não localizado, reentrega e mudou-se

respostas = [
            #0 Endereço não localizado
            "@\n\nFavor verificar.\n\nFomos na entrega da NF em assunto e o endereço não foi localizado.\n\nGentileza confirmar o endereço e caso o mesmo estiver divergente, favor: \n\n1- Autorizar o custo de reentrega de 50% do valor do CT-e origem; \n2-Nos encaminhar uma CC-e para endereço correto;  \n3-Informar um contato válido do cliente para alinhar nova tentativa de entrega.\n\nAguardamos um breve retorno a fim de evitar impactos no prazo de entrega previsto para o cliente.\n",
            #1 Reentrega    
            "@\n\nFavor verificar.\n\nFomos na entrega da NF em assunto e o destinatário estava ausente.\nPara seguir com uma nova tentativa de entrega, precisaremos do seguinte: \n\n1- Autorização para custo de reentrega (50% do valor do CT-e origem) \n2- Um contato válido do cliente para alinharmos.\n3- Caso o endereço esteja divergente favor nos encaminhar uma CC-e para o local correto também.\n\nAguardamos um breve retorno a fim de evitar impactos no prazo de entrega previsto para o cliente.\n",           
            #2 Estadia
            "@\n\nFavor verificar e auxiliar.\n\nEstamos na entrega da NF em assunto aguardando descarregar.\n\nChegada: \nSaída: ",
            #3 Mudou-se
            "@\n\nFomos na entrega da NF em assunto e nos informaram que o cliente mudou-se.\nGentileza verificar e nos encaminhar: \n\n1-Uma CC-e para o endereço correto; \n2-Autorizar o custo de reentrega de 50% do valor do CT-e origem. \n3-Caso o endereço seja em outro estado, será cobrado um novo frete.\n\nAguardamos breve retorno a fim de não prejudicar o prazo de entrega do cliente.",
            #4 Recusa por pendência
            "@\n\nDurante a tentativa de entrega da NF em questão, o cliente recusou o recebimento alegando que havia uma pendência no documento.\nSolicitamos, por gentileza, a verificação da situação e o devido posicionamento quanto ao procedimento a ser adotado.\n\nInformamos que:\n\nEm caso de reentrega, será aplicada uma taxa adicional correspondente a 50% do valor do CT-e de origem;\n\nEm caso de devolução, será aplicada uma taxa correspondente a 100% do valor do CT-e de origem."
]

agendamento = [
            #0 informar agendamento
            "\n@\n\nA mercadoria da NF em assunto está agendada para dia  \nGentileza confirmar ciência.",
            #1 Verificar retorno agendamento
            "\nEsta mercadoria segue conforme agenda amanhã?"

]

respostasWpp = [
    #0
    "\n\nTudo bem por aqui. E você?\n\nVou verificar agora, só um momento.", 
    #1
    "\n\nVou verificar agora, só um momento.",
    #2
    "\n\nTudo bem?",
    #3
    "\n\nPreciso de um auxílio com esta NF: ",
    #4
    "\n\nSegue e-mail referente a NF: ",
    #5
    "\nPor gentileza, teria o PDF desta NF ou o número da mesma para eu verificar melhor?\n"
]

diversos = [
    #0 e-mail
    "sac.blu@arletetransportes.com.br",
    #1
    "\nMercadoria entregue segue comprovante.",
    #2
    "\nEsta mercadoria está em rota de entrega hoje, deve ser finalizada em horário comercial até as 18h.",
    #3
    "\nTemos retorno sobre este caso?",
    #4
    "\n\n\n",
    #5
    "\n\n@\n\nReentrega em sistema-anexo.\n\nGentileza informar nova previsão.",
    #6
    "\n\n@\n\nReentrega e CC-e em sistema-anexo.\n\nGentileza informar nova previsão.",
    #7
    "Vamos precisar dos dados de quem irá retirar:\n\nNome Completo: \n\nRG ou CPF: \n\nPlaca do veículo: ",
    #3
    "\n\n@\n\nGentileza verificar.",
    #4
    "\n\n@\n\nGentileza solicitar agendamento de coleta e *informar a data*."
       
]

endereco = [
    #1
    "Filial - BLUMENAU (BLU / CD) - \n\nRodovia Ingo Henring, 8979 CNPJ: 72.090.442/0009-34\n\nBairro: Margem Esquerda \n\nCep: 89116-755 - Gaspar/SC \n\nFone:(47) 3318-0980\n\nContato: blumenau@arletetransportes.com.br \n\nhttps://www.google.com/maps?q=-26.9167197,-48.9699487"
]

# Corrigindo a lógica de hora
hora_atual = datetime.now().hour

if hora_atual < 12:
    saudacao = "Olá! Bom dia."
elif hora_atual < 18:
    saudacao = "Olá! Boa tarde."
else:
    saudacao = "Olá! Boa noite."

#Funções INICIO***********************************************************

def recusaPorPendencia():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(respostas[4])
    pyautogui.hotkey("ctrl","v")

def agendarColeta():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(diversos[9])
    pyautogui.hotkey("ctrl","v")

def verificar():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(diversos[8])
    pyautogui.hotkey("ctrl","v")

def baseBlu():
    pyperclip.copy(endereco[0])
    pyautogui.hotkey("ctrl","v")

def dadosRetira():
   
    pyperclip.copy(diversos[7])
    pyautogui.hotkey("ctrl","v")

def reentragaECCe():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(diversos[6])
    pyautogui.hotkey("ctrl", "v")

def reentregaEmS():

    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(diversos[5])
    pyautogui.hotkey("ctrl", "v")
    
def endNaoLocalizado():
        
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(diversos[4])
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(respostas[0])
    pyautogui.hotkey("ctrl","v")
  
def reentrega():

    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(diversos[4])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostas[1])
    pyautogui.hotkey("ctrl","v")
   
def estadia():

    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(diversos[4])
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(respostas[2])
    pyautogui.hotkey("ctrl", "v")
  
def saudar():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(respostasWpp[2])
    pyautogui.hotkey("ctrl", "v")

def wpp():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[0])
    pyautogui.hotkey("ctrl", "v")

def wppVouVerificar():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostasWpp[1])
    pyautogui.hotkey("ctrl", "v")

def wppAuxilioNf():

    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(respostasWpp[2])
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(respostasWpp[3])
    pyautogui.hotkey("ctrl", "v")

def wppSegueEmail():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")
    pyperclip.copy(respostasWpp[4])
    pyautogui.hotkey("ctrl","v")

def wppMercEmRota():
    pyperclip.copy(diversos[2])
    pyautogui.hotkey("ctrl","v")

def falarEmail():
    pyperclip.copy(diversos[0])
    pyautogui.hotkey("ctrl","v")
    
def mercadoriaEntregue():

    pyperclip.copy(diversos[1])
    pyautogui.hotkey("ctrl", "v")

def cobrar2():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(diversos[4])
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(diversos[3])
    pyautogui.hotkey("ctrl","v")

def mudouSe():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")

    pyperclip.copy(diversos[4])
    pyautogui.hotkey("ctrl", "v")
    
    pyperclip.copy(respostas[3])
    pyautogui.hotkey("ctrl","v")

def agendar():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(diversos[4])
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(agendamento[0])
    pyautogui.hotkey("ctrl", "v")

def cobrarAgAm():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(diversos[4])
    pyautogui.hotkey("ctrl", "v")

    pyperclip.copy(agendamento[1])
    pyautogui.hotkey("ctrl", "v")

def pdfOuNumNF():
    pyperclip.copy(respostasWpp[5])
    pyautogui.hotkey("ctrl", "v")

def reentregaECCe():
    pyperclip.copy(saudacao)
    pyautogui.hotkey("ctrl","v")
    pyperclip.copy(diversos[4])
    pyautogui.hotkey("ctrl","v")

#Funções FIM ***********************************************************

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
        if "//0" in comando_digitado:
            apagar_comando(3)
            saudar()
            comando_digitado = ""

        elif "//1" in comando_digitado:
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
       #email*************************************************************************
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

        elif "//q" in comando_digitado:
            apagar_comando(4)
            recusaPorPendencia()
            comando_digitado = ""
            
        elif "//7" in comando_digitado:
            apagar_comando(3)
            mercadoriaEntregue()
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
        
        elif "//ag" in comando_digitado:
            apagar_comando(4)
            agendar()
            comando_digitado = ""

        elif "//ca" in comando_digitado:
            apagar_comando(4)
            cobrarAgAm()
            comando_digitado = ""
        
        elif "//p" in comando_digitado:
            apagar_comando(3)
            pdfOuNumNF()
            comando_digitado = ""
        
        elif "//*" in comando_digitado:
            apagar_comando(3)
            reentregaEmS()
            comando_digitado = ""
        
        elif "//-" in comando_digitado:
            apagar_comando(3)
            reentregaECCe()
            comando_digitado = ""
        
        elif "//b" in comando_digitado:
            apagar_comando(3)
            baseBlu()
            comando_digitado = ""
        
        elif "//d" in comando_digitado:
            apagar_comando(3)
            dadosRetira()
            comando_digitado = ""

        elif "//g" in comando_digitado:
            apagar_comando(3)
            verificar()
            comando_digitado = ""

        elif "///" in comando_digitado:
            apagar_comando(3)
            agendarColeta()
            comando_digitado = ""

        elif len(comando_digitado) > 10:
            comando_digitado = ""



keyboard.on_press(verificar_comando)
mostrar_comandos()
print("Monitorando comandos digitados como //1, //2, etc...")
keyboard.wait