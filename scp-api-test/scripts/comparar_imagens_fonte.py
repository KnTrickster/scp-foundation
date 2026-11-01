import csv
import re
from urllib.parse import unquote

from caminhos import PASTA_RELATORIOS
from dados import iterar_registros
from inventariar_midias import EXTENSOES_IMAGEM, extensao_url, urls_do_texto

ARQUIVO_SAIDA = PASTA_RELATORIOS / "diferenca_imagens.csv"

EXTENSOES = r"(?:png|jpe?g|gif|webp|svg)"

# Valor de um parâmetro de imagem: |name=arquivo.png, |url=arquivo.png, image=..., src=...
PADRAO_PARAMETRO = re.compile(
    r"\b(?:name|url|image|src)\s*=\s*([^\s|\[\]]+?\." + EXTENSOES + r")(?=[\s|\]]|$)",
    re.IGNORECASE,
)

# Sintaxe direta: [[image arquivo.png ...]], [[=image ...]], [[<image ...]], [[f<image ...]]
PADRAO_DIRETO = re.compile(
    r"\[\[\s*[=<>f]*image\s+([^\s|\[\]]+?\." + EXTENSOES + r")(?=[\s|\]]|$)",
    re.IGNORECASE,
)


def normalizar(nome):
    """Reduz um nome ou URL de imagem ao nome do arquivo, comparável entre fontes."""
    nome = nome.strip()
    for _ in range(2):  # alguns links vêm codificados duas vezes (%252C)
        nome = unquote(nome)
    nome = nome.split("?")[0].rstrip("/").rsplit("/", 1)[-1]
    nome = re.sub(r"^(?:file|image|ficheiro):", "", nome, flags=re.IGNORECASE)
    return nome.replace(" ", "_").lower()


def imagens_declaradas_na_fonte(fonte):
    encontrados = PADRAO_PARAMETRO.findall(fonte) + PADRAO_DIRETO.findall(fonte)
    return {normalizar(nome) for nome in encontrados}


def main():
    linhas = []

    for chave, registro in iterar_registros():
        html = registro.get("raw_content") or ""
        fonte = registro.get("raw_source") or ""
        imagens = registro.get("images") or []

        nomes_api = {normalizar(str(url)) for url in imagens if url}
        urls = urls_do_texto(html) | urls_do_texto(fonte)
        nomes_urls = {
            normalizar(url) for url in urls if extensao_url(url) in EXTENSOES_IMAGEM
        }
        nomes_fonte = imagens_declaradas_na_fonte(fonte)

        faltando = sorted(nomes_fonte - nomes_api - nomes_urls)
        linhas.append({
            "designacao": registro.get("scp") or chave,
            "imagens_api": len(nomes_api),
            "imagens_inventario": len(nomes_api | nomes_urls),
            "imagens_declaradas_na_fonte": len(nomes_fonte),
            "faltando_qtd": len(faltando),
            "faltando_nomes": " | ".join(faltando),
        })

    with ARQUIVO_SAIDA.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]), delimiter=";")
        escritor.writeheader()
        escritor.writerows(linhas)

    com_diferenca = [linha for linha in linhas if linha["faltando_qtd"] > 0]
    print(f"Registros analisados: {len(linhas)}")
    print(f"Registros com imagens declaradas na fonte que o inventário não vê: {len(com_diferenca)}")
    print(f"Total de arquivos de imagem não vistos: {sum(l['faltando_qtd'] for l in linhas)}")
    print("\nMaiores diferenças:")
    for linha in sorted(com_diferenca, key=lambda l: -l["faltando_qtd"])[:15]:
        print(f"  {linha['designacao']}: {linha['faltando_qtd']} -> {linha['faltando_nomes'][:120]}")
    print(f"\nRelatório: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()