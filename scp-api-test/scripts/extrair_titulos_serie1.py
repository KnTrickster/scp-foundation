import json
import re

from bs4 import BeautifulSoup

from caminhos import ARQUIVO_INDICE, ARQUIVO_TITULOS

# Aceita o final do link: "scp-173", "173" ou "902-warning"
PADRAO_DESTINO = re.compile(r"^(?:scp-)?(\d{3,4})(?:-warning)?$", re.IGNORECASE)

def carregar_html_do_hub(caminho, nome_hub="scp-series"):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        hubs = json.load(arquivo)

    hub = hubs.get(nome_hub)
    if hub is None:
        raise ValueError(f"Hub '{nome_hub}' não encontrado em {caminho}.")

    return hub.get("raw_content", "")

def designacao_pelo_link(href):
    destino = href.rstrip("/").split("/")[-1]
    correspondencia = PADRAO_DESTINO.match(destino)
    if not correspondencia:
        return None
    return f"SCP-{correspondencia.group(1)}"

def extrair_titulos(html):
    soup = BeautifulSoup(html, "html.parser")
    titulos = {}
    sem_designacao = []  # links que não apontam para um artigo SCP numerado
    repetidos = []

    for item in soup.find_all("li"):
        link = item.find("a", href=True)
        if not link:
            continue

        designacao = designacao_pelo_link(link["href"])
        if designacao is None:
            sem_designacao.append(link["href"])
            continue

        if designacao in titulos:
            repetidos.append(designacao)

        titulos[designacao] = item.get_text(" ", strip=True)

    return titulos, sem_designacao, repetidos

def main():
    html = carregar_html_do_hub(ARQUIVO_INDICE)
    titulos, sem_designacao, repetidos = extrair_titulos(html)

    with open(ARQUIVO_TITULOS, "w", encoding="utf-8") as arquivo:
        json.dump(titulos, arquivo, ensure_ascii=False, indent=2)

    print(f"Títulos extraídos: {len(titulos)}")
    print(f"Arquivo gerado: {ARQUIVO_TITULOS}")

    print(f"\nLinks sem designação reconhecida: {len(sem_designacao)}")
    for href in sem_designacao[:10]:
        print(f"  {href}")
    if len(sem_designacao) > 10:
        print(f"  ... e mais {len(sem_designacao) - 10}")

    print(f"\nDesignações repetidas no índice: {len(repetidos)}")
    for designacao in repetidos:
        print(f"  {designacao}")

    print("\nPrimeiros 10 resultados:")
    for designacao, titulo in list(titulos.items())[:10]:
        print(f"  {designacao}: {titulo}")


if __name__ == "__main__":
    main()