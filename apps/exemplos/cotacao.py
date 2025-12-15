
import json
import os
import threading
import time
import logging
from datetime import datetime
from typing import Callable, Dict, Any

import pyperclip
import pyautogui
import keyboard

# ---------- Config ----------
COMMANDS_FILE = "comandos_custom.json"
LOG_FILE = "sac11.log"
KEY_BUFFER_MAX = 50         # quantos caracteres guardamos no buffer
BACKSPACE_DELAY = 0.01      # delay entre backspaces para apagar o comando digitado
PASTE_DELAY = 0.05          # delay entre colagens (para estabilidade)
# ----------------------------

# Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("sac11")
logger.info("Inicializando sac11.py")

# ------------------------
# Conteúdos e dados fixos
# ------------------------
# Mensagens e arrays que você já tinha (mantive e limpei)
respostas = [
    #1
    "*Hemilly:*\nCotação: \nValor do frete: \nPrevisão de entrega em dias úteis: \n",

]

# Saudação baseada na hora
def obter_saudacao() -> str:
    hora = datetime.now().hour
    if hora < 12:
        return "*Hemilly:*\nOlá! Bom dia."
    elif hora < 18:
        return "*Hemilly:*\nOlá! Boa tarde."
    else:
        return "*Hemilly:*\nOlá! Boa noite."

saudacao = obter_saudacao()

# ------------------------
# Utilitários de ação
# ------------------------
def enviar(*mensagens: str, pause: float = PASTE_DELAY) -> None:
    """
    Copia e cola cada mensagem na ordem usando pyperclip + hotkey.
    Usa pequeno delay entre colagens para estabilidade.
    """
    for msg in mensagens:
        try:
            pyperclip.copy(msg)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(pause)
        except Exception as e:
            logger.exception("Falha ao colar mensagem: %s", e)

def apagar_comando(tamanho: int) -> None:
    """
    Apaga 'tamanho' caracteres usando backspace. Usa pyautogui.press para melhor compatibilidade.
    """
    try:
        for _ in range(max(0, tamanho)):
            pyautogui.press("backspace")
            time.sleep(BACKSPACE_DELAY)
    except Exception as e:
        logger.exception("Falha ao apagar comando: %s", e)

# ------------------------
# Funções já existentes (refatoradas para usar enviar)
# ------------------------

def cotacao():
    enviar(respostas[0])

def email():
    enviar(saudacao, respostas[1])

# --------------------------------
# Sistema de comandos (dinâmico)
# --------------------------------
# Comandos built-in que chamam funções.
BUILTIN_COMMANDS: Dict[str, Callable[[], None]] = {
    "//0": cotacao,
    
}

# Carregamento de comandos customizados (mensagens)
def load_custom_commands(path: str = COMMANDS_FILE) -> Dict[str, Dict[str, Any]]:
    """
    Retorna dict do tipo:
      { "//x": { "mensagem": "texto...", "include_saudacao": True } }
    """
    if not os.path.exists(path):
        logger.info("Arquivo de comandos custom não encontrado, criando vazio.")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info("Comandos custom carregados: %d", len(data))
            return data
    except Exception as e:
        logger.exception("Erro ao carregar comandos customizados: %s", e)
        return {}

def save_custom_commands(data: Dict[str, Dict[str, Any]], path: str = COMMANDS_FILE) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Comandos custom salvos: %d", len(data))
    except Exception as e:
        logger.exception("Erro ao salvar comandos customizados: %s", e)

# Carrega comandos custom no startup
CUSTOM_COMMANDS = load_custom_commands()

def execute_custom_command(cmd: str) -> None:
    """
    Colocar mensagem custom do arquivo JSON. KeyError tratado externamente.
    Estrutura do item:
      { "mensagem": "...", "include_saudacao": True/False }
    """
    try:
        item = CUSTOM_COMMANDS.get(cmd)
        if not item:
            logger.warning("Comando custom não encontrado ao executar: %s", cmd)
            return
        mensagem = item.get("mensagem", "")
        include_s = item.get("include_saudacao", True)
        if include_s:
            enviar(saudacao, mensagem)
        else:
            enviar(mensagem)
    except Exception:
        logger.exception("Erro ao executar comando custom %s", cmd)

# Funções para adicionar/remover comandos custom via script (ou GUI)
def add_custom_command(cmd: str, mensagem: str, include_saudacao: bool = True) -> bool:
    """
    Adiciona comando custom; retorna True se adicionado, False se já existe.
    """
    if cmd in BUILTIN_COMMANDS or cmd in CUSTOM_COMMANDS:
        logger.warning("Tentativa de adicionar comando que já existe: %s", cmd)
        return False
    CUSTOM_COMMANDS[cmd] = {"mensagem": mensagem, "include_saudacao": include_saudacao}
    save_custom_commands(CUSTOM_COMMANDS)
    logger.info("Comando custom adicionado: %s", cmd)
    return True

def remove_custom_command(cmd: str) -> bool:
    if cmd in CUSTOM_COMMANDS:
        del CUSTOM_COMMANDS[cmd]
        save_custom_commands(CUSTOM_COMMANDS)
        logger.info("Comando custom removido: %s", cmd)
        return True
    logger.warning("Tentativa de remover comando inexistente: %s", cmd)
    return False

# Construção do dicionário de comandos ativos (merge)
def get_all_command_keys_sorted() -> list:
    """
    Retorna lista de comandos (strings) ordenados por tamanho decrescente.
    Isso garante que comandos longos como //sg sejam detectados antes de //s, por exemplo.
    """
    keys = list(BUILTIN_COMMANDS.keys()) + list(CUSTOM_COMMANDS.keys())
    keys = sorted(set(keys), key=lambda s: len(s), reverse=True)
    return keys

# ------------------------
# Listener de teclado
# ------------------------
class CommandListener:
    def __init__(self):
        self.buffer = ""   # buffer de caracteres recentes
        self.lock = threading.Lock()
        self.running = False

    def start(self):
        logger.info("Iniciando listener de teclado em thread.")
        self.running = True
        keyboard.on_press(self.on_press)
        # Não bloqueamos aqui; keyboard.wait() será chamado no fim do script.
        # Executamos em thread separada somente para lógica que precise de loop.
        # keyboard.on_press já opera com callbacks em background.
        logger.info("Listener iniciado.")

    def stop(self):
        logger.info("Parando listener.")
        self.running = False
        keyboard.unhook_all()

    def on_press(self, e):
        """
        Callback quando qualquer tecla é pressionada.
        Construímos um buffer simples com representação legível (barra = '/').
        """
        try:
            name = e.name  # geralmente string
            ch = ""
            # Normalização básica:
            if len(name) == 1:
                ch = name
            elif name == "space":
                ch = " "
            elif name == "enter":
                ch = "\n"
            elif name in ("slash", "/"):
                ch = "/"
            elif name == "backspace":
                # remover último char do buffer
                with self.lock:
                    self.buffer = self.buffer[:-1]
                return
            else:
                # teclas especiais ignoradas
                return

            with self.lock:
                self.buffer += ch
                # limitar tamanho do buffer
                if len(self.buffer) > KEY_BUFFER_MAX:
                    self.buffer = self.buffer[-KEY_BUFFER_MAX:]

                # verificar se algum comando está presente (prioridade para strings mais longas)
                all_cmds = get_all_command_keys_sorted()
                for cmd in all_cmds:
                    if cmd in self.buffer:
                        logger.info("Comando detectado: %s", cmd)
                        # Apagar o que o usuário digitou (apagar o próprio comando visível)
                        try:
                            apagar_comando(len(cmd))
                        except Exception:
                            logger.exception("Falha ao apagar comando visível: %s", cmd)
                        # Executar comando
                        # builtin
                        if cmd in BUILTIN_COMMANDS:
                            try:
                                BUILTIN_COMMANDS[cmd]()
                            except Exception:
                                logger.exception("Erro ao executar função builtin do comando %s", cmd)
                        # custom
                        elif cmd in CUSTOM_COMMANDS:
                            try:
                                execute_custom_command(cmd)
                            except Exception:
                                logger.exception("Erro ao executar comando custom %s", cmd)
                        # reset buffer
                        self.buffer = ""
                        return
        except Exception:
            logger.exception("Erro no on_press do listener.")

# ------------------------
# Execução principal
# ------------------------
def main():
    logger.info("Inicializando aplicação principal.")
    # Start listener
    listener = CommandListener()
    listener.start()
    print("Monitorando comandos. Digite seus comandos (ex: //1, //sg, //x)...")
    logger.info("Aplicação pronta - aguardando teclas.")
    try:
        # keyboard.wait() bloqueia o thread principal até ctrl+c (ou outro evento)
        keyboard.wait()
    except KeyboardInterrupt:
        logger.info("Interrupção por teclado (KeyboardInterrupt).")
    except Exception:
        logger.exception("Erro inesperado no main.")
    finally:
        listener.stop()
        logger.info("Encerrando sac11.py")

if __name__ == "__main__":
    main()
