import pyperclip
import re
import time
import keyboard

# ================= CONFIGURAÇÃO =================

TECLA_TOGGLE = ";"
INTERVALO = 0.3

# ================= ESTADO =================

ativo = False

# ================= FUNÇÕES =================

def contem_letras(texto: str) -> bool:
    return bool(re.search(r"[A-Za-z]", texto))


def contem_numeros(texto: str) -> bool:
    return bool(re.search(r"\d", texto))


def limpar_numeros(texto: str) -> str:
    """
    Remove tudo que NÃO for número
    """
    return re.sub(r"[^\d]", "", texto)


def alternar_estado():
    global ativo
    ativo = not ativo
    estado = "ATIVADO" if ativo else "DESATIVADO"
    print(f"[CLIPBOARD NUMÉRICO] {estado}")


def monitorar_clipboard():
    ultimo_texto = None

    print("[INFO] Monitoramento iniciado")
    print("[INFO] Pressione PAUSE BREAK para ligar/desligar")

    while True:
        if not ativo:
            time.sleep(INTERVALO)
            continue

        try:
            texto_atual = pyperclip.paste()

            # Ignora se não mudou
            if texto_atual == ultimo_texto:
                time.sleep(INTERVALO)
                continue

            # Atualiza referência ORIGINAL
            ultimo_texto = texto_atual

            # Regras de processamento
            if not texto_atual:
                continue

            # ❌ Se tiver letras → NÃO mexe
            if contem_letras(texto_atual):
                continue

            # ❌ Se não tiver números → NÃO mexe
            if not contem_numeros(texto_atual):
                continue

            texto_limpo = limpar_numeros(texto_atual)

            # Só substitui se realmente mudou
            if texto_limpo and texto_limpo != texto_atual:
                pyperclip.copy(texto_limpo)
                print(f"[NUMÉRICO LIMPO] {texto_atual} → {texto_limpo}")

        except Exception as e:
            print(f"[ERRO] {e}")

        time.sleep(INTERVALO)

# ================= HOTKEY =================

keyboard.add_hotkey(TECLA_TOGGLE, alternar_estado)

# ================= START =================

monitorar_clipboard()
