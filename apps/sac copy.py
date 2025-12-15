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

# ================== CONFIG ==================
COMMANDS_FILE = "comandos_custom.json"
LOG_FILE = "sac11.log"

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
logger.info("Inicializando programa.py")
# ============================================

# ================== ESTADO GLOBAL ==================
command_queue = Queue()
clipboard_filter_enabled = False
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
    "@\n\nDurante a tentativa de entrega da NF em questão, o cliente recusou o recebimento alegando que havia uma pendência no documento.\nSolicitamos, por gentileza, a verificação da situação e o devido posicionamento quanto ao procedimento a ser adotado.\n\nInformamos que:\n\nEm caso de reentrega, será aplicada uma taxa adicional correspondente a 50% do valor do CT-e de origem;\n\nEm caso de devolução, será aplicada uma taxa correspondente a 100% do valor do CT-e de origem."
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
    "\n\nTudo bem?",
    #3
    "\n\nPreciso de um auxílio com esta NF: ",
    #4
    "\n\nSegue e-mail referente a NF: ",
    #5
    "\nPor gentileza, teria o PDF desta NF ou o número da mesma para eu verificar melhor?\n",
    #6
    "Por nada, eu é que agradeço! Se precisar, estou à disposição.\n",
    #7
    "Muito obrigado!",
    #8
    "\n\nComo posso ajudar você hoje?"
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
    #8
    "\n\n@\n\nGentileza verificar.",
    #9
    "\n\n@\n\nGentileza solicitar agendamento de coleta e *informar a data*."
]

endereco = [
    #1
    "Arlete Transportes Filial (BLU)  - \n\nRodovia Ingo Henring, 8979 CNPJ: 72.090.442/0009-34\n\nBairro: Margem Esquerda \n\nCep: 89116-755 - Gaspar/SC \n\nFone:(47) 3318-0980\n\nContato: blumenau@arletetransportes.com.br \n\nhttps://www.google.com/maps?q=-26.9167197,-48.9699487"
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
def ajudar():
    enviar(respostasWpp[8])

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
    enviar(saudacao,respostasWpp[2], respostasWpp[4])

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
    "//a": ajudar,
    "//1": wpp,
    "//2": wppVouVerificar,
    "//3": wppAuxilioNf,
    "//4": reentrega,
    "//5": endNaoLocalizado,
    "//6": mudouSe,
    "//q": recusaPorPendencia,
    "//7": mercadoriaEntregue,
    "//8": cobrar2,
    "//9": estadia,
    "//e": falarEmail,
    "//r": wppMercEmRota,
    "//se": wppSegueEmail,
    "//ag": agendar,
    "//ar": agendar,         # se desejar diferente, ajuste
    "//ca": cobrarAgAm,
    "//p": pdfOuNumNF,
    "//*": reentregaEmS,
    "//-": reentragaECCe,
    "//b": baseBlu,
    "//d": dadosRetira,
    "//g": verificar,
    "///": agendarColeta,
    "//+": agradecimento,
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
    while True:
        cmd = command_queue.get()
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
    while True:
        if clipboard_filter_enabled:
            text = pyperclip.paste()
            if text != last_text:
                # Só filtra se for número com caracteres especiais
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
    estado = "ATIVADO" if clipboard_filter_enabled else "DESATIVADO"
    print(f"[Filtro Numérico] {estado}")
    logger.info("Filtro numérico %s", estado)

keyboard.add_hotkey("pause", toggle_clipboard_filter)
# ============================================

# ================== MAIN ==================
def main():
    print("sac11 ativo.")
    print("• Comandos automáticos: //x")
    print("• Pause/Break liga/desliga filtro numérico")
    logger.info("Aplicação pronta.")
    keyboard.wait()

if __name__ == "__main__":
    main()
# ============================================
