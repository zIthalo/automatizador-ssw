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
    "\n\n@\n\nDurante a tentativa de entrega da NF em questão, o cliente recusou o recebimento alegando que havia uma pendência no documento.\nSolicitamos, por gentileza, a verificação da situação e o devido posicionamento quanto ao procedimento a ser adotado.\n\nInformamos que:\n\nEm caso de reentrega, será aplicada uma taxa adicional correspondente a 50% do valor do CT-e de origem;\n\nEm caso de devolução, será aplicada uma taxa correspondente a 100% do valor do CT-e de origem."
]

agendamento = [
    #0 informar agendamento
    "@\n\nA mercadoria da NF em assunto está agendada para dia  \nGentileza confirmar ciência.",
    #1 Verificar retorno agendamento
    "\nEsta mercadoria segue conforme agenda amanhã?"
]

respostasWpp = [
    #0
    "\n\nTudo bem por aqui. E você?\n\nVou verificar agora, só um momento.",
    #1
    "\n\nVou verificar agora, só um momento.",
    #2
    "\n\nTudo bem?\n\nComo posso ajudar você?",
    #3
    "\n\nTudo bem?\n\nPreciso de um auxílio com esta NF: ",
    #4
    "\n\nTudo bem?\n\nSegue e-mail referente a NF: \n\nPoderia nos auxiliar?",
    #5
    "\nPor gentileza, teria o PDF desta NF ou o número da mesma para eu verificar melhor?\n",
    #6
    "Por nada, eu é que agradeço! Se precisar, estou à disposição.\n",
    #7
    "Muito obrigado!",
    #8
    "\n\nTudo bem por aqui e você?\n\nComo posso te ajudar hoje?",
    #9
    "A mercadoria está com previsão de entrega para dia ",
    #10
    "Vou verificar e já te retorno.",
    #11
    "Olá!\n\nEstamos conversando sobre a NF: \n\nVou verificar e já te retorno.",
]

diversos = [
    #0 e-mail
    "sac.blu@arletetransportes.com.br",
    #1
    "\nMercadoria entregue segue comprovante.",
    #2
    "\nEsta mercadoria está em rota de entrega hoje, deve ser finalizada em horário comercial.",
    #3
    "\nTemos retorno sobre este caso?",
    #4
    "\n\n\n",
    #5
    "\n\n@\n\nGentileza emitir CT-e de reentrega para a NF em assunto e CT-e: ",
    #6
    "\n\n@\n\nFavor emitir CT-e de reentrega para a NF em assunto e CT-e: \n\n@\n\nCC-e em sistema-anexo.",
    #7
    "Vamos precisar dos dados da pessoa que irá retirar:\n\nNome Completo: \n\nRG ou CPF: \n\nPlaca do veículo: ",
    #8
    "\n\n@\n\nGentileza verificar.",
    #9
    "\n\n@\n\nGentileza solicitar agendamento de coleta e *informar a data*.",
    #10
    "Remetente acionado. Aguardo retorno.",
    #11
    "Em tratativas.",
    "\n\n@\n\nFavor verificar e autorizar custos abaxo:\n\ncusto: R$ \n\n-Impostos: R$ \n\n -Total: R$ \n\nAguardo retorno para darmos prosseguimento.\n",
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
def estamosConversandoSobreaNf():
    enviar(respostasWpp[11])

def repassarCustos():
    enviar(saudacao, diversos[12])

def jaRetorno():
    enviar(respostasWpp[10])

def previsaoDeEntrega():
    enviar(saudacao, diversos[9])

def acionadoRemetente():
    enviar(diversos[10])

def emTratativas():
    enviar(diversos[11])

def tudoBemComoPossoTeAjudar():
    enviar(saudacao, respostasWpp[8])

def dizerObrigado():
    enviar(respostasWpp[7])

def agradecimento():
    enviar(respostasWpp[6])

def recusaPorPendencia():
    enviar(saudacao, respostas[4])

def agendarColeta():
    enviar(saudacao, diversos[9])

def verificar():
    enviar(saudacao, diversos[8])

def baseBlu():
    enviar(endereco[0])

def dadosRetira():
    enviar(diversos[7])

def reentragaECCe():
    enviar(saudacao, diversos[6])

def reentregaEmS():
    enviar(saudacao, diversos[5])

def endNaoLocalizado():
    enviar(saudacao, diversos[4], respostas[0])

def reentrega():
    enviar(saudacao, diversos[4], respostas[1])

def estadia():
    enviar(saudacao, diversos[4], respostas[2])

def saudar():
    enviar(saudacao, respostasWpp[2])

def wpp():
    enviar(saudacao, respostasWpp[0])

def wppVouVerificar():
    enviar(saudacao, respostasWpp[1])

def wppAuxilioNf():
    enviar(saudacao, respostasWpp[3])

def wppSegueEmail():
    enviar(saudacao, respostasWpp[4])

def wppMercEmRota():
    enviar(diversos[2])

def falarEmail():
    enviar(diversos[0])

def mercadoriaEntregue():
    enviar(diversos[1])

def cobrar2():
    enviar(saudacao, diversos[4], diversos[3])

def mudouSe():
    enviar(saudacao, diversos[4], respostas[3])

def agendar():
    enviar(saudacao, diversos[4], agendamento[0])

def cobrarAgAm():
    enviar(saudacao, diversos[4], agendamento[1])

def pdfOuNumNF():
    enviar(respostasWpp[5])

def reentregaECCe_alt():
    enviar(saudacao, diversos[4])

def agendamento_colet():
    enviar(saudacao, "Agendamento confirmado.")

BUILTIN_COMMANDS: Dict[str, Callable[[], None]] = {
    "//0": saudar,
    "//1": wpp,
    "//2": wppVouVerificar,
    "//3": wppAuxilioNf,
    "//4": reentrega,
    "//5": endNaoLocalizado,
    "//6": mudouSe,
    "//7": recusaPorPendencia,
    "//8": cobrar2,
    "//9": estadia,
    "///": agendarColeta,
    "**0": tudoBemComoPossoTeAjudar,
    "**1": wppSegueEmail,
    "**2": wppMercEmRota,
    "**3": mercadoriaEntregue,
    "**4": previsaoDeEntrega,
    "**5": pdfOuNumNF,
    "**6": falarEmail,
    "**7": baseBlu,
    "**8": dadosRetira,
    "**9": agradecimento,
    "***": agendar,
    "--0": jaRetorno,
    "--1": repassarCustos,
    "--2": estamosConversandoSobreaNf,
    "--3": acionadoRemetente,
    "--4": emTratativas,
    "---": verificar,
    "//ca": cobrarAgAm,
    "//*": reentregaEmS,
    "//-": reentragaECCe,
    "//.": dizerObrigado,
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
