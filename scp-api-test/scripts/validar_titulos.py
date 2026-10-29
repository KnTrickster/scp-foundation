import json
import re
import sys

from caminhos import ARQUIVO_TITULOS

PADRAO_SIMPLES = re.compile(r"^SCP-(\d{3,4})$")

def parte_do_titulo(designacao, texto):
    """Remove a designação do texto e devolve só o que sobra."""
    resto = re.sub(re.escape(designacao), "", texto, count=1, flags=re.IGNORECASE)
    return resto.strip(" -–—:\t")

def main():
    with open(ARQUIVO_TITULOS, "r", encoding="utf-8") as arquivo:
        titulos = json.load(arquivo)

    problemas = 0
    print(f"Total de títulos: {len(titulos)}")

    # 1. Texto vazio ou sem nada além da designação
    sem_titulo = [d for d, t in titulos.items() if not parte_do_titulo(d, t)]
    print(f"Sem título após a designação: {len(sem_titulo)}")
    problemas += len(sem_titulo)

    # 2. Designações fora do formato esperado (variantes como SCP-049-J)
    simples = {}
    variantes = []
    for designacao in titulos:
        correspondencia = PADRAO_SIMPLES.match(designacao)
        if correspondencia:
            simples[int(correspondencia.group(1))] = designacao
        else:
            variantes.append(designacao)
    print(f"Designações com sufixo ou formato diferente: {len(variantes)}")
    for designacao in variantes:
        print(f"  {designacao}")

    # 3. Números faltando no intervalo da Series 1 (1 a 999)
    faltantes = sorted(set(range(1, 1000)) - set(simples))
    print(f"Números ausentes entre 1 e 999: {len(faltantes)}")
    for numero in faltantes:
        print(f"  SCP-{numero:03d}")
    problemas += len(faltantes)

    # 4. Títulos informativos (não são erro)
    marcados = [d for d, t in titulos.items()
                if parte_do_titulo(d, t).upper() in ("N/A", "[ACCESS DENIED]")]
    print(f"Títulos N/A ou [ACCESS DENIED] (revisão manual): {len(marcados)}")

    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()