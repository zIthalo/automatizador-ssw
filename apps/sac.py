#!/usr/bin/env python3
# sac11.py
# Reescrito: sistema de comandos dinâmico, persistência JSON, logging, listener em thread.
# Compatível com Python 3.13.2
#
# Instruções:
# 1) Instale dependências (se ainda não instaladas):
#    pip install pyautogui keyboard pyperclip
# 2) Faça backup do seu sac11.py antigo.
# 3) Coloque este arquivo na mesma pasta onde deseja rodar.
# 4) Execute: python sac11.py
#
# Arquivos auxiliares gerados automaticamente:
# - comandos_custom.json   -> comandos adicionados pelo usuário (mensagens)
# - sac11.log              -> log de execução
#
# Observações:
# - Comandos embutidos (funções existentes) ainda usam saudação quando adequado.
# - Comandos personalizados (do JSON) colam apenas a mensagem gravada.
# - Para gerenciar comandos via GUI, mantenha o gerenciador separado (sac11_manager.py).
#
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

# Saudação baseada na hora
def obter_saudacao() -> str:
    hora = datetime.now().hour
    if hora < 12:
        return "Olá! Bom dia."
    elif hora < 18:
        return "Olá! Boa tarde."
    else:
        return "Olá! Boa noite."

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

# --------------------------------
# Sistema de comandos (dinâmico)
# --------------------------------
# Comandos built-in que chamam funções.
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
