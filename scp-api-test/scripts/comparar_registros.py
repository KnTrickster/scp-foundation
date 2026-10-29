import json

import ijson

from caminhos import ARQUIVO_CONTEUDO, ARQUIVO_TITULOS


def carregar_titulos():
    with open(ARQUIVO_TITULOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def ler_identificadores_api(caminho):
    """Lê o JSON grande em streaming e guarda só os campos de identificação."""
    registros = {}
    ignorados = []

    with open(caminho, "rb") as arquivo:
        for chave, registro in ijson.kvitems(arquivo, ""):
            if not chave.upper().startswith("SCP-") or not isinstance(registro, dict):
                ignorados.append(chave)
                continue

            registros[chave.upper()] = {
                campo: registro.get(campo)
                for campo in ("scp", "title", "scp_number", "link", "url")
            }

    return registros, ignorados


def procurar_em_outros_campos(designacao, registros):
    """Procura uma designação (formato SCP-NNN) nos demais campos, não só na chave."""
    numero = int(designacao.removeprefix("SCP-"))
    alvos = {f"SCP-{numero:03d}", f"SCP-{numero}"}

    for chave, campos in registros.items():
        try:
            if int(campos["scp_number"]) == numero:
                return chave, "scp_number"
        except (TypeError, ValueError):
            pass

        for campo in ("scp", "link", "url"):
            valor = str(campos.get(campo) or "").rstrip("/").split("/")[-1]
            if valor.upper() in alvos:
                return chave, campo

    return None, None


def main():
    titulos = carregar_titulos()
    registros, ignorados = ler_identificadores_api(ARQUIVO_CONTEUDO)

    designacoes_titulos = set(titulos)
    designacoes_api = set(registros)

    sem_titulo = sorted(designacoes_api - designacoes_titulos)
    sem_registro = sorted(designacoes_titulos - designacoes_api)

    print("=== RESUMO ===")
    print(f"Títulos extraídos: {len(designacoes_titulos)}")
    print(f"Registros SCP na API: {len(designacoes_api)}")
    print(f"Chaves da API ignoradas (não são SCP-*): {len(ignorados)}")
    print(f"Registros da API sem título: {len(sem_titulo)}")
    print(f"Títulos sem registro na API (pela chave): {len(sem_registro)}")

    print("\n=== REGISTROS DA API SEM TÍTULO ===")
    for designacao in sem_titulo:
        print(f"  {designacao}")

    print("\n=== TÍTULOS SEM REGISTRO NA API ===")
    for designacao in sem_registro:
        chave, campo = procurar_em_outros_campos(designacao, registros)
        if chave:
            print(f"  {designacao}: encontrado em outro campo ({campo}) -> {chave}")
        else:
            print(f"  {designacao}: não encontrado em nenhum campo")


if __name__ == "__main__":
    main()