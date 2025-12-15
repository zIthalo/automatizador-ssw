import pyperclip
import re
import time
import keyboard

monitorando = False  # Variável de controle para ativar/desativar o monitoramento

def limpar_texto(texto):
    # Substitui apenas os separadores dentro de sequências numéricas
    texto_processado = re.sub(r'(\d)[.,:/\s+*#-_](\d)', r'\1\2', texto)
    return texto_processado

def monitorar_clipboard():
    global monitorando
    texto_anterior = ""

    while True:
        if monitorando:  # Só executa se estiver ativado
            texto_atual = pyperclip.paste()
            if texto_atual != texto_anterior:
                texto_limpo = limpar_texto(texto_atual)
                pyperclip.copy(texto_limpo)
                print(f"Texto processado: {texto_limpo}")
                texto_anterior = texto_atual
            time.sleep(1)  # Aguarda um segundo antes de verificar novamente
        else:
            time.sleep(0.2)  # Aguarda um pouco para evitar consumo excessivo de CPU

def alternar_monitoramento():
    global monitorando
    monitorando = not monitorando
    estado = "ativado" if monitorando else "desativado"
    print(f"Monitoramento {estado}")

# Configura o evento para a tecla F10
keyboard.add_hotkey("f10", alternar_monitoramento)

print("Pressione F10 para alternar o monitoramento.")
monitorar_clipboard()

#1.23.5