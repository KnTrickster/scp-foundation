import csv

from caminhos import PASTA_RELATORIOS
from dados import carregar_titulos

ARQUIVO_SAIDA = PASTA_RELATORIOS / "relatorio_triagem.csv"

# Sinais que merecem revisão, não exclusão automática.
INDICADORES = {
    "STAFF PLACEHOLDER": "PLACEHOLDER",
    "N/A": "POSSIBLE_NA",
    "ACCESS DENIED": "POSSIBLE_RESTRICTED",
    "ACESSO BLOQUEADO": "POSSIBLE_RESTRICTED",
}


def triar(titulos):
    resultados = []

    for designacao, texto in titulos.items():
        texto_maiusculo = texto.upper()
        alertas = [
            categoria
            for indicador, categoria in INDICADORES.items()
            if indicador in texto_maiusculo
        ]

        resultados.append({
            "designacao": designacao,
            "titulo_extraido": texto,
            "alertas": ";".join(alertas) if alertas else "NENHUM",
            "revisao_manual": "SIM" if alertas else "NAO",
        })

    return resultados


def main():
    resultados = triar(carregar_titulos())

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=list(resultados[0]), delimiter=";"
        )
        escritor.writeheader()
        escritor.writerows(resultados)

    com_alertas = sum(1 for r in resultados if r["alertas"] != "NENHUM")
    print("Triagem concluída.")
    print(f"Registros analisados: {len(resultados)}")
    print(f"Com alertas: {com_alertas}")
    print(f"Relatório: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()