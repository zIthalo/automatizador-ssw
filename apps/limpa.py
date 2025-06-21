import pyperclip
import re
import time


def limpar_texto(texto):
    # Reorganizando os caracteres para evitar erro de intervalo
    caracteres_remover = r"[.,:/\s+*#-]"
    return re.sub(caracteres_remover, "", texto)


def monitorar_clipboard():
    texto_anterior = ""
    while True:
        texto_atual = pyperclip.paste()  # Obtém o texto atual da área de transferência
        if texto_atual != texto_anterior:  # Verifica se houve uma mudança
            texto_limpo = limpar_texto(texto_atual)  # Limpa o texto
            pyperclip.copy(texto_limpo)  # Substitui na área de transferência
            print(f"Texto processado: {texto_limpo}")
            texto_anterior = texto_atual

        time.sleep(1)  # Aguarda um segundo antes de verificar novamente


# Inicia o monitoramento
monitorar_clipboard()
