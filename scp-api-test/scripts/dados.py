import json
import re

import ijson

from caminhos import ARQUIVO_CONTEUDO, ARQUIVO_TITULOS


def carregar_titulos():
    with open(ARQUIVO_TITULOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def iterar_registros(caminho=ARQUIVO_CONTEUDO):
    """Entrega (designação, registro) um por vez, sem carregar o arquivo inteiro."""
    with open(caminho, "rb") as arquivo:
        for chave, registro in ijson.kvitems(arquivo, ""):
            if isinstance(registro, dict):
                yield chave, registro


def parte_do_titulo(texto):
    """'SCP-173 - The Sculpture' -> 'The Sculpture'. Funciona com PDG-213 etc."""
    partes = re.split(r"\s+[-–—]\s+", texto, maxsplit=1)
    return partes[1].strip() if len(partes) == 2 else ""