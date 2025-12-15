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
logger.info("Inicializando sac11.py")
# ============================================

# ================== ESTADO GLOBAL ==================
command_queue = Queue()
clipboard_filter_enabled = False
# ==================================================

# ================== MENSAGENS ==================
respostas = [
    "*Hemilly:*\nCotação:\nValor do frete:\nPrevisão de entrega:\n",
]

def obter_saudacao() -> str:
    hora = datetime.now().hour
    if hora < 12:
        return "*Hemilly:*\nOlá! Bom dia."
    elif hora < 18:
        return "*Hemilly:*\nOlá! Boa tarde."
    else:
        return "*Hemilly:*\nOlá! Boa noite."

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
def cotacao():
    enviar(respostas[0])

BUILTIN_COMMANDS: Dict[str, Callable[[], None]] = {
    "//0": cotacao,
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
