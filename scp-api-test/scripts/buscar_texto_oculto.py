import csv
import re

from bs4 import BeautifulSoup

from caminhos import PASTA_RELATORIOS
from dados import iterar_registros

ARQUIVO_SAIDA = PASTA_RELATORIOS / "texto_oculto.csv"

# font-size: 0 / 0px / 0.0em / 0% (com ou sem unidade, com ou sem !important)
PADRAO_FONTE_ZERO = re.compile(
    r"font-size\s*:\s*0+(?:\.0+)?\s*(?:px|pt|em|rem|%)?\s*(?:!important)?\s*(?:;|$)",
    re.IGNORECASE,
)


def buscar_texto_oculto(registros):
    encontrados = []

    for designacao, registro in registros:
        html = registro.get("raw_content") or ""
        soup = BeautifulSoup(html, "html.parser")

        for elemento in soup.select("[style]"):
            estilo = elemento.get("style", "")
            if PADRAO_FONTE_ZERO.search(estilo):
                texto = elemento.get_text(" ", strip=True)
                encontrados.append({
                    "designacao": designacao,
                    "estilo": estilo,
                    "tamanho_texto": len(texto),
                    "trecho": texto[:180],  # só para o terminal, não vai ao CSV
                })

    return encontrados


def main():
    encontrados = buscar_texto_oculto(iterar_registros())

    # O CSV não leva o texto do artigo, só a localização do achado.
    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=["designacao", "estilo", "tamanho_texto"],
            delimiter=";",
            extrasaction="ignore",
        )
        escritor.writeheader()
        escritor.writerows(encontrados)

    registros_afetados = sorted({item["designacao"] for item in encontrados})
    print(f"Registros com fonte de tamanho zero: {len(registros_afetados)}")
    print(f"Elementos encontrados: {len(encontrados)}")
    print(f"Registros: {', '.join(registros_afetados)}")
    print(f"Relatório: {ARQUIVO_SAIDA}")

    for item in encontrados[:30]:
        print(f"\n{item['designacao']} | {item['estilo']}")
        print(item["trecho"] or "[sem texto]")


if __name__ == "__main__":
    main()