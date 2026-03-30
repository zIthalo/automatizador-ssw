# -*- coding: utf-8 -*-

import json
import os
import threading
import time
import logging
import re
from datetime import datetime
from queue import Queue
from typing import Callable, Dict, Any

import pyperclip
import pyautogui
import keyboard
import tkinter as tk
from tkinter import messagebox

# ================== PATH BASE ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMANDS_FILE = os.path.join(BASE_DIR, "comandos_custom.json")
LOG_FILE = os.path.join(BASE_DIR, "sac11.log")

# ================== CONFIG ==================
KEY_BUFFER_MAX = 50
BACKSPACE_DELAY = 0.01
PASTE_DELAY = 0.05

# ================== LOG ==================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("sac11")

# ================== ESTADO ==================
command_queue = Queue()
clipboard_filter_enabled = False
app_running = True

# ================== FORMATADOR ==================
def formatar_texto_usuario(texto: str) -> str:
    return texto.replace("\n", "\\n\\n")

# ================== SAUDAÇÃO ==================
def obter_saudacao():
    h = datetime.now().hour
    if h < 12:
        return "Bom dia."
    elif h < 18:
        return "Boa tarde."
    return "Boa noite."

# ================== UTIL ==================
def enviar(*msgs):
    for msg in msgs:
        if isinstance(msg, bytes):
            msg = msg.decode("utf-8", errors="ignore")

        # Força correção de encoding bugado
        try:
            msg = msg.encode("latin1").decode("utf-8")
        except:
            pass

        pyperclip.copy(msg)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(PASTE_DELAY)

def apagar_comando(t):
    for _ in range(t):
        pyautogui.press("backspace")
        time.sleep(BACKSPACE_DELAY)

# ================== MENSAGENS ==================
mensagens = [
    #0
    "\n\nTudo bem?\n\nComo posso ajudar você?",
    #1
    "\n\nTudo bem por aqui. E você?\n\nVerificando, só um momento.",
    #2
    "\n\nVerificando, só um momento.",
    #3
    "\n\nTudo bem?\n\nPreciso de um auxílio com esta NF: ",
    #4
    "\n\nTudo bem?\n\nSegue e-mail referente a NF: \n\nPoderia nos auxiliar?",
    #5
    "\n\nTudo bem por aqui! E você?\n\nComo posso ajudar você hoje?",
    #6
    "Por gentileza, teria o PDF desta NF? \n\nOu teria o número da nota fiscal para eu verificar melhor?",
    #7
    "Por nada, eu é quem agradeço! \n\nSe precisar, pode chamar estou à disposição.",
    #8
    "Muito obrigado!",
    #9
    "A mercadoria está com previsão de entrega para dia ",
    #10
    "Vou verificar e já te retorno.",
    #11
    "sac.blu@arletetransportes.com.br",
    #12 
    "Mercadoria entregue segue comprovante.",
    #13
    "Esta mercadoria está em rota de entrega hoje, deve ser finalizada em horário comercial. \n\nSerá entregue no endereço acima.",
    #14
    "Vamos precisar dos dados da pessoa que irá retirar:\n\nNome Completo: \n\nRG ou CPF: \n\nPlaca do veículo: ",   
    #15
    "Cliente acionado, aguardando retorno.",
    #16
    "Verificando / Cobrando retorno.",
    #17
    "Base acionada, aguardando retorno.",
    #18
    "Olá!\n\nEstamos conversando sobre a NF: \n\nVou verificar e já te retorno.",
    #19
    "\n\nReentrega em sistema,\n\nGentileza informar a nova previsão",
    #20
    "\n\nReentrega e CC-e em sistema.\n\nGentileza informar a nova previsão.",
    #21
    "\n\n@\n\nGentileza verificar."
  
]

endereco = [
    #1
    "Arlete Transportes Filial (BLU)  - \n\nRodovia Ingo Henring, 8979 CNPJ: 72.090.442/0009-34\n\nBairro: Margem Esquerda \n\nCep: 89116-755 - Gaspar/SC \n\nFone:(47) 3318-0980\n\nContato: blumenau@arletetransportes.com.br \n\nhttps://www.google.com/maps?q=-26.9167197,-48.9699487",
    
]

# ================== FUNÇÕES ==================
def wpp0(): enviar(obter_saudacao(), mensagens[0])
def wpp1(): enviar(obter_saudacao(), mensagens[1])
def wpp2(): enviar(obter_saudacao(), mensagens[2])
def wpp0():
    enviar(obter_saudacao(), mensagens[0])
def wpp1():
    enviar(obter_saudacao(), mensagens[1])
def wpp2():
    enviar(obter_saudacao(), mensagens[2])
def wpp3():
    enviar(obter_saudacao(), mensagens[3])
def wpp4():
    enviar(obter_saudacao(), mensagens[4])
def wpp5():
    enviar(obter_saudacao(), mensagens[5])
def wpp6():
    enviar(obter_saudacao(), mensagens[6])
def wpp7():
    enviar(obter_saudacao(), mensagens[7])
def wpp8():
    enviar(obter_saudacao(), mensagens[8])
def wpp9():
    enviar(obter_saudacao(), mensagens[9])
def wpp10():
    enviar(mensagens[10])
def wpp11():
    enviar(mensagens[11])
def wpp12():
    enviar(mensagens[12])
def wpp13():
    enviar(mensagens[13])
def wpp14():
    enviar(mensagens[14])
def wpp15():
    enviar(mensagens[15])
def wpp16():
    enviar(mensagens[16])
def wpp17():
    enviar(mensagens[17])
def wpp18():
    enviar(mensagens[18])
def wpp19():
    enviar(obter_saudacao(), mensagens[19])
def wpp20():
    enviar(obter_saudacao(), mensagens[20])
def wpp21():
    enviar(obter_saudacao(), mensagens[21])
def wpp22():
    enviar(endereco[0])

BUILTIN_COMMANDS = {
    "//0": wpp0, #tudo bem? como posso ajudar você?
    "//1": wpp1, #tudo bem por aqui. E você? Verificando,
    "//2": wpp2, #verificando
    "//3": wpp3, #auxílio com NF.
    "//4": wpp4, # segue e-mail referente
    "//5": wpp5, # Como posso ajudar você hoje?
    "//6": wpp6, # teria o PDF desta NF?
    "//+": wpp7, # por nada.
    "//.": wpp8, # muito obrigado!
    "**.": wpp9, # previsão de entrega
    "**0": wpp10, # já te retorno.
    "**1": wpp11, # sac.blu
    "**2": wpp12, # segue comprovante.
    "**3": wpp13, # rota de entrega hoje
    "**5": wpp15, # cliente acionado.
    "**6": wpp16, # verificando.
    "**7": wpp17, # base acionada
    "--1": wpp19, # reentrega
    "--2": wpp20, # reentrega e CC-e
    "--3": wpp21, # gentileza verificar.
    "//b": wpp22, # endereço base blu
    "//d": wpp14, # dados da pessoa que irá retirar.
    "--4": wpp18, # estamos conversando sobre a NF: 
}

# ================== CUSTOM ==================
def load_custom():
    if not os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, "w") as f:
            json.dump({}, f)
        return {}
    with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_custom():
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(CUSTOM_COMMANDS, f, indent=2, ensure_ascii=False)

CUSTOM_COMMANDS = load_custom()

def execute_custom(cmd):
    item = CUSTOM_COMMANDS.get(cmd)
    if not item:
        return

    msg = item["mensagem"].replace("\\n\\n", "\n\n")

    if item.get("include_saudacao", True):
        enviar(obter_saudacao(), msg)
    else:
        enviar(msg)

# ================== LISTA ==================
def get_all():
    return sorted(set(BUILTIN_COMMANDS)|set(CUSTOM_COMMANDS), key=len, reverse=True)

# ================== WORKER ==================
def worker():
    while app_running:
        try:
            cmd = command_queue.get(timeout=0.5)
        except:
            continue

        if cmd in BUILTIN_COMMANDS:
            BUILTIN_COMMANDS[cmd]()
        elif cmd in CUSTOM_COMMANDS:
            execute_custom(cmd)

        command_queue.task_done()

threading.Thread(target=worker, daemon=True).start()

# ================== LISTENER ==================
class Listener:
    def __init__(self):
        self.buffer = ""

    def on_press(self, e):
        if not app_running: return

        n = e.name
        if len(n)==1: ch=n
        elif n in ("slash","/"): ch="/"
        elif n=="backspace":
            self.buffer=self.buffer[:-1]
            return
        else: return

        self.buffer += ch
        self.buffer = self.buffer[-KEY_BUFFER_MAX:]

        for cmd in get_all():
            if cmd in self.buffer:
                apagar_comando(len(cmd))
                command_queue.put(cmd)
                self.buffer=""
                return

keyboard.on_press(Listener().on_press)

# ================== GUI ==================
def abrir_config():
    win = tk.Toplevel(root)
    win.title("Configurações")

    tk.Button(win,text="Nova",command=criar).pack(pady=5)
    tk.Button(win,text="Editar",command=editar).pack(pady=5)
    tk.Button(win,text="Deletar",command=deletar).pack(pady=5)
    tk.Button(win,text="Listar",command=listar).pack(pady=5)
    tk.Button(win,text="Voltar",command=win.destroy).pack(pady=10)

# ================== CRUD ==================
def criar():
    w=tk.Toplevel(root)

    tk.Label(w,text="Comando").pack()
    cmd=tk.Entry(w); cmd.pack()

    tk.Label(w,text="Mensagem").pack()
    txt=tk.Text(w,height=8); txt.pack()

    var=tk.BooleanVar(value=True)
    tk.Checkbutton(w,text="Saudação",variable=var).pack()

    def salvar():
        CUSTOM_COMMANDS[cmd.get()] = {
            "mensagem": formatar_texto_usuario(txt.get("1.0","end").strip()),
            "include_saudacao": var.get()
        }
        save_custom()
        w.destroy()

    tk.Button(w,text="Salvar",command=salvar).pack()
    tk.Button(w,text="Voltar",command=w.destroy).pack()

def listar():
    w=tk.Toplevel(root)
    t=tk.Text(w); t.pack()

    for c,d in CUSTOM_COMMANDS.items():
        t.insert("end", f"{c} -> {d['mensagem'].replace('\\n\\n','\\n')}\n\n")

def deletar():
    w=tk.Toplevel(root)
    lb=tk.Listbox(w); lb.pack()

    for c in CUSTOM_COMMANDS: lb.insert("end",c)

    def delcmd():
        c=lb.get(tk.ACTIVE)
        del CUSTOM_COMMANDS[c]
        save_custom()
        lb.delete(tk.ACTIVE)

    tk.Button(w,text="Deletar",command=delcmd).pack()
    tk.Button(w,text="Voltar",command=w.destroy).pack()

def editar():
    w=tk.Toplevel(root)
    lb=tk.Listbox(w); lb.pack()

    for c in CUSTOM_COMMANDS: lb.insert("end",c)

    def open_edit():
        c=lb.get(tk.ACTIVE)
        item=CUSTOM_COMMANDS[c]

        e=tk.Toplevel(w)
        txt=tk.Text(e); txt.pack()
        txt.insert("1.0", item["mensagem"].replace("\\n\\n","\n"))

        def salvar():
            CUSTOM_COMMANDS[c]["mensagem"]=formatar_texto_usuario(txt.get("1.0","end"))
            save_custom()
            e.destroy()

        tk.Button(e,text="Salvar",command=salvar).pack()

    tk.Button(w,text="Editar",command=open_edit).pack()
    tk.Button(w,text="Voltar",command=w.destroy).pack()

# ================== ROOT ==================
root = tk.Tk()
root.title("Mensagens Automáticas")
root.geometry("360x200")

tk.Label(root,text="Sistema ativo").pack(pady=10)

tk.Button(root,text="⚙️",command=abrir_config).place(x=320,y=10)

def sair():
    global app_running
    app_running=False
    keyboard.unhook_all()
    root.destroy()

tk.Button(root,text="Sair",command=sair).pack(pady=20)

root.mainloop()