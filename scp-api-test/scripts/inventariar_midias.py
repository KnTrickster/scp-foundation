import csv
import re
from collections import Counter
from pathlib import Path

from caminhos import PASTA_RELATORIOS
from dados import iterar_registros

ARQUIVO_SAIDA = PASTA_RELATORIOS / "inventario_midias.csv"

EXTENSOES_AUDIO = {".mp3", ".ogg", ".wav", ".m4a", ".flac", ".opus", ".aac"}
EXTENSOES_VIDEO = {".mp4", ".webm", ".mov", ".m4v", ".ogv"}
EXTENSOES_IMAGEM = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

# URLs completas (http/https) ou arquivos locais da própria wiki.
# Não aceita "//" sozinho: no Wikidot isso é a marcação de itálico.
PADRAO_URL = re.compile(
    r"""https?://[^\s"'<>]+|/?local--files/[^\s"'<>]+""",
    re.IGNORECASE,
)

PADRAO_TAGS = re.compile(
    r"<\s*(audio|video|iframe|embed|object)\b",
    re.IGNORECASE,
)


def limpar_url(url):
    return url.rstrip(".,;:!?)]}")


def extensao_url(url):
    """Extensão do arquivo no fim da URL, sem validar a URL inteira."""
    caminho = re.split(r"[?#]", url, maxsplit=1)[0].lower()
    nome = caminho.rsplit("/", 1)[-1]
    return Path(nome).suffix


def urls_do_texto(texto):
    if not isinstance(texto, str):
        return set()
    return {limpar_url(url) for url in PADRAO_URL.findall(texto)}


def lista_imagens(registro):
    imagens = registro.get("images", [])
    if not isinstance(imagens, list):
        return []
    return [str(url) for url in imagens if url]


def urls_com_extensao(urls, extensoes):
    return sorted(url for url in urls if extensao_url(url) in extensoes)


def analisar_registro(designacao, registro):
    html = registro.get("raw_content", "") or ""
    fonte = registro.get("raw_source", "") or ""
    urls = urls_do_texto(html) | urls_do_texto(fonte)

    imagens = lista_imagens(registro)
    audios = urls_com_extensao(urls, EXTENSOES_AUDIO)
    videos = urls_com_extensao(urls, EXTENSOES_VIDEO)
    imagens_por_url = urls_com_extensao(urls, EXTENSOES_IMAGEM)

    tags = Counter(tag.lower() for tag in PADRAO_TAGS.findall(html))

    # Sinaliza possíveis casos para inspeção, não exclusão automática.
    revisar = bool(
        audios
        or videos
        or tags
        or len(imagens) != len(set(imagens))
    )

    return {
        "designacao": registro.get("scp") or designacao,
        "titulo_api": registro.get("title", ""),
        "url_pagina": registro.get("url", ""),
        "imagens_api_qtd": len(imagens),
        "imagens_api_urls": " | ".join(imagens),
        "outras_urls_imagem": " | ".join(imagens_por_url),
        "audios_urls": " | ".join(audios),
        "videos_urls": " | ".join(videos),
        "tags_audio_video_embed_object": str(dict(tags)),
        "revisao_manual": "SIM" if revisar else "NAO",
    }


def main():
    resultados = [
        analisar_registro(chave, registro)
        for chave, registro in iterar_registros()
    ]

    campos = list(resultados[0].keys()) if resultados else []

    with ARQUIVO_SAIDA.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        escritor.writeheader()
        escritor.writerows(resultados)

    com_imagens = sum(int(item["imagens_api_qtd"]) > 0 for item in resultados)
    com_audio = sum(bool(item["audios_urls"]) for item in resultados)
    com_video = sum(bool(item["videos_urls"]) for item in resultados)
    para_revisao = sum(item["revisao_manual"] == "SIM" for item in resultados)

    print("\n=== INVENTÁRIO DE MÍDIA ===")
    print(f"Registros analisados: {len(resultados)}")
    print(f"Registros com imagens na API: {com_imagens}")
    print(f"Registros com URLs de áudio reconhecidas: {com_audio}")
    print(f"Registros com URLs de vídeo reconhecidas: {com_video}")
    print(f"Registros sinalizados para revisão: {para_revisao}")
    print(f"\nRelatório salvo em: {ARQUIVO_SAIDA}")
    print("Nenhum conteúdo foi alterado ou baixado.")


if __name__ == "__main__":
    main()