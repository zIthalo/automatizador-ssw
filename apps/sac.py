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
# ============================================

# ================== LOGGING ==================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("sac11")
logger.info("Inicializando sac11.py")
# ============================================

# ================== ESTADO GLOBAL ==================
command_queue = Queue()
clipboard_filter_enabled = False
app_running = True
# ==================================================

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
    "\n\nReentrega em sistema,\n\nGetileza informar a nova previsão",
    #20
    "\n\nReentrega e CC-e em sistema.\n\nGetileza informar a nova previsão.",
    #21
    "\n\n@\n\nGentileza verificar."
  
]

endereco = [
    #1
    "Arlete Transportes Filial (BLU)  - \n\nRodovia Ingo Henring, 8979 CNPJ: 72.090.442/0009-34\n\nBairro: Margem Esquerda \n\nCep: 89116-755 - Gaspar/SC \n\nFone:(47) 3318-0980\n\nContato: blumenau@arletetransportes.com.br \n\nhttps://www.google.com/maps?q=-26.9167197,-48.9699487",
    
]
def obter_saudacao() -> str:
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia."
    elif hora < 18:
        return "Boa tarde."
    else:
        return "Boa noite."

saudacao = obter_saudacao()
# ==============================================

# ================== UTILITÁRIOS ==================
def enviar(*mensagens: str):
    for msg in mensagens:
        pyperclip.copy(msg)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(PASTE_DELAY)

def apagar_comando(tamanho: int):
    for _ in range(tamanho):
        pyautogui.press("backspace")
        time.sleep(BACKSPACE_DELAY)
# ================================================

# ================== FUNÇÕES ==================

def wpp0():
    enviar(saudacao, mensagens[0])
def wpp1():
    enviar(saudacao, mensagens[1])
def wpp2():
    enviar(saudacao, mensagens[2])
def wpp3():
    enviar(saudacao, mensagens[3])
def wpp4():
    enviar(saudacao, mensagens[4])
def wpp5():
    enviar(saudacao, mensagens[5])
def wpp6():
    enviar(saudacao, mensagens[6])
def wpp7():
    enviar(saudacao, mensagens[7])
def wpp8():
    enviar(saudacao, mensagens[8])
def wpp9():
    enviar(saudacao, mensagens[9])
def wpp10():
    enviar(saudacao, mensagens[10])
def wpp11():
    enviar(saudacao, mensagens[11])
def wpp12():
    enviar(saudacao, mensagens[12])
def wpp13():
    enviar(saudacao, mensagens[13])
def wpp14():
    enviar(saudacao, mensagens[14])
def wpp15():
    enviar(saudacao, mensagens[15])
def wpp16():
    enviar(saudacao, mensagens[16])
def wpp17():
    enviar(saudacao, mensagens[17])
def wpp18():
    enviar(saudacao, mensagens[18])
def wpp19():
    enviar(saudacao, mensagens[19])
def wpp20():
    enviar(saudacao, mensagens[20])
def wpp21():
    enviar(saudacao, mensagens[21])
def wpp22():
    enviar(saudacao, endereco[0])



BUILTIN_COMMANDS: Dict[str, Callable[[], None]] = {
    "//0": wpp0,
    "//1": wpp1,
    "//2": wpp2,
    "//3": wpp3,
    "//4": wpp4,
    "//5": wpp5,
    "//6": wpp6,
    "//+": wpp7,
    "//.": wpp8,
    "**.": wpp9,
    "**0": wpp10,
    "**1": wpp11,
    "**2": wpp12,
    "**3": wpp13,
    "**4": wpp14,
    "**5": wpp15,
    "**6": wpp16,
    "**7": wpp17,
    "**8": wpp18,
    "**9": wpp19,
    "--0": wpp20,
    "--1": wpp21,
    "--2": wpp22,
}
# =============================================

# ================== COMANDOS CUSTOM ==================
def load_custom_commands():
    if not os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)
        return {}
    with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

CUSTOM_COMMANDS = load_custom_commands()

def execute_custom_command(cmd: str):
    item = CUSTOM_COMMANDS.get(cmd)
    if not item:
        return
    if item.get("include_saudacao", True):
        enviar(saudacao, item["mensagem"])
    else:
        enviar(item["mensagem"])
# ====================================================

def get_all_commands_sorted():
    return sorted(
        set(BUILTIN_COMMANDS.keys()) | set(CUSTOM_COMMANDS.keys()),
        key=len,
        reverse=True
    )

# ================== WORKER ==================
def command_worker():
    while app_running:
        try:
            cmd = command_queue.get(timeout=0.5)
        except:
            continue
        try:
            if cmd in BUILTIN_COMMANDS:
                BUILTIN_COMMANDS[cmd]()
            elif cmd in CUSTOM_COMMANDS:
                execute_custom_command(cmd)
        except Exception:
            logger.exception("Erro ao executar comando %s", cmd)
        finally:
            command_queue.task_done()

threading.Thread(target=command_worker, daemon=True).start()
# ============================================

# ================== LISTENER ==================
class CommandListener:
    def __init__(self):
        self.buffer = ""

    def on_press(self, e):
        if not app_running:
            return

        name = e.name
        if len(name) == 1:
            ch = name
        elif name in ("slash", "/"):
            ch = "/"
        elif name == "backspace":
            self.buffer = self.buffer[:-1]
            return
        else:
            return

        self.buffer += ch
        self.buffer = self.buffer[-KEY_BUFFER_MAX:]

        for cmd in get_all_commands_sorted():
            if cmd in self.buffer:
                apagar_comando(len(cmd))
                command_queue.put(cmd)
                self.buffer = ""
                return

listener = CommandListener()
keyboard.on_press(listener.on_press)
# ============================================

# ================== CLIPBOARD FILTER ==================
def clipboard_cleaner():
    last_text = ""
    while app_running:
        if clipboard_filter_enabled:
            text = pyperclip.paste()
            if text != last_text:
                if re.search(r"\d", text) and not re.search(r"[a-zA-Z]", text):
                    cleaned = re.sub(r"\D+", "", text)
                    if cleaned:
                        pyperclip.copy(cleaned)
                last_text = text
        time.sleep(0.3)

threading.Thread(target=clipboard_cleaner, daemon=True).start()
# =====================================================

# ================== TOGGLE ==================
def toggle_clipboard_filter():
    global clipboard_filter_enabled
    clipboard_filter_enabled = not clipboard_filter_enabled
    status_var.set(
        "Filtro numérico: ATIVADO" if clipboard_filter_enabled else "Filtro numérico: DESATIVADO"
    )
    logger.info("Filtro numérico %s", clipboard_filter_enabled)

keyboard.add_hotkey("pause", toggle_clipboard_filter)
# ============================================

# ================== INTERFACE GRÁFICA ==================
def sair():
    global app_running
    if messagebox.askyesno("Sair", "Deseja realmente encerrar o programa?"):
        app_running = False
        keyboard.unhook_all()
        root.destroy()

root = tk.Tk()
root.title("Programa – Mensagens Automáticas")
root.geometry("360x200")
root.resizable(False, False)

tk.Label(
    root,
    text="Programa ativo em segundo plano",
    font=("Segoe UI", 12, "bold")
).pack(pady=10)

tk.Label(
    root,
    text="• Comandos: //x\n• Pause/Break liga/desliga filtro numérico",
    justify="left"
).pack(pady=5)

status_var = tk.StringVar(value="Filtro numérico: DESATIVADO")
tk.Label(root, textvariable=status_var).pack(pady=5)

tk.Button(
    root,
    text="Sair",
    width=15,
    command=sair
).pack(pady=15)

# ================== MAIN ==================
logger.info("Interface iniciada.")
root.mainloop()
logger.info("Aplicação encerrada.")

#CÓDIGOS SEM USO OU PARA REUTILIZAÇÃO:

#respostas = [
    #0 Endereço não localizado
    # "@\n\nFavor verificar.\n\nFomos na entrega da NF em assunto e o endereço não foi localizado.\n\nGentileza confirmar o endereço e caso o mesmo estiver divergente, favor: \n\n1- Autorizar o custo de reentrega de 50% do valor do CT-e origem; \n2-Nos encaminhar uma CC-e para endereço correto;  \n3-Informar um contato válido do cliente para alinhar nova tentativa de entrega.\n\nAguardamos um breve retorno a fim de evitar impactos no prazo de entrega previsto para o cliente.\n",
    #1 Reentrega
    # "@\n\nFavor verificar.\n\nFomos na entrega da NF em assunto e o destinatário estava ausente.\nPara seguir com uma nova tentativa de entrega, precisaremos do seguinte: \n\n1- Autorização para custo de reentrega (50% do valor do CT-e origem) \n2- Um contato válido do cliente para alinharmos.\n3- Caso o endereço esteja divergente favor nos encaminhar uma CC-e para o local correto também.\n\nAguardamos um breve retorno a fim de evitar impactos no prazo de entrega previsto para o cliente.\n",
    #2 Estadia
    # "@\n\nFavor verificar e auxiliar.\n\nEstamos na entrega da NF em assunto aguardando descarregar.\n\nChegada: \nSaída: ",
    #3 Mudou-se
    # "@\n\nFomos na entrega da NF em assunto e nos informaram que o cliente mudou-se.\nGentileza verificar e nos encaminhar: \n\n1-Uma CC-e para o endereço correto; \n2-Autorizar o custo de reentrega de 50% do valor do CT-e origem. \n3-Caso o endereço seja em outro estado, será cobrado um novo frete.\n\nAguardamos breve retorno a fim de não prejudicar o prazo de entrega do cliente.",
    #4 Recusa por pendência
    #"\n\n@\n\nDurante a tentativa de entrega da NF em questão, o cliente recusou o recebimento alegando que havia uma pendência no documento.\nSolicitamos, por gentileza, a verificação da situação e o devido posicionamento quanto ao procedimento a ser adotado.\n\nInformamos que:\n\nEm caso de reentrega, será aplicada uma taxa adicional correspondente a 50% do valor do CT-e de origem;\n\nEm caso de devolução, será aplicada uma taxa correspondente a 100% do valor do CT-e de origem."
#]

# agendamento = [
#     #0 informar agendamento
#     "@\n\nA mercadoria da NF em assunto está agendada para dia  \nGentileza confirmar ciência.",
#     #1 Verificar retorno agendamento
#     "\nEsta mercadoria segue conforme agenda amanhã?"
# ]