import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PREFIXO = "x_1902920_scp_fo_0_"


def pasta_do_app(raiz):
    propriedades = raiz / "sn_source_control.properties"
    for linha in propriedades.read_text(encoding="utf-8").splitlines():
        if linha.startswith("path="):
            return raiz / linha.split("=", 1)[1].strip().strip("/")
    raise SystemExit("Linha 'path=' não encontrada em sn_source_control.properties.")


def valor(registro, tag):
    elemento = registro.find(tag)
    return (elemento.text or "").strip() if elemento is not None else ""


def numero(texto):
    return int(texto) if texto.isdigit() else 0


def arquivos(pasta_app, prefixo):
    for subpasta in ("update", "author_elective_update"):
        yield from sorted((pasta_app / subpasta).glob(f"{prefixo}*.xml"))


def resumir_colunas(pasta_app):
    cabecalho = ["Table", "Column", "Type", "Max", "Mandatory", "Read-only",
                 "Unique", "Default", "Reference", "Cascade", "Display",
                 "Action", "Folder"]
    linhas = []

    for caminho in arquivos(pasta_app, "sys_dictionary_"):
        raiz = ET.parse(caminho).getroot()
        for reg in raiz.iter("sys_dictionary"):
            coluna = valor(reg, "element")
            if not coluna:
                continue  # entrada da própria tabela
            linhas.append([
                valor(reg, "name").replace(PREFIXO, ""),
                coluna,
                valor(reg, "internal_type"),
                valor(reg, "max_length"),
                valor(reg, "mandatory"),
                valor(reg, "read_only"),
                valor(reg, "unique"),
                valor(reg, "default_value"),
                valor(reg, "reference").replace(PREFIXO, ""),
                valor(reg, "reference_cascade_rule"),
                valor(reg, "display"),
                reg.get("action", ""),
                caminho.parent.name,
            ])

    print("## Columns\n")
    print("| " + " | ".join(cabecalho) + " |")
    print("|" + "---|" * len(cabecalho))
    for linha in sorted(linhas):
        print("| " + " | ".join(linha) + " |")


def resumir_choices(pasta_app):
    print("\n## Choices")
    for caminho in arquivos(pasta_app, "sys_choice_"):
        raiz = ET.parse(caminho).getroot()
        opcoes = list(raiz.iter("sys_choice"))
        if not opcoes:
            tags = sorted({elemento.tag for elemento in raiz.iter()})
            print(f"\n{caminho.name}: nenhum <sys_choice> encontrado. Tags: {tags}")
            continue

        primeira = opcoes[0]
        tabela = valor(primeira, "name").replace(PREFIXO, "")
        print(f"\n{tabela}.{valor(primeira, 'element')}")
        for opcao in sorted(opcoes, key=lambda o: numero(valor(o, "sequence"))):
            inativa = " (inactive)" if valor(opcao, "inactive") == "true" else ""
            print(f"  {valor(opcao, 'sequence'):>3}  "
                  f"{valor(opcao, 'value')} = {valor(opcao, 'label')}{inativa}")


def main():
    raiz = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    pasta_app = pasta_do_app(raiz)
    print(f"App folder: {pasta_app.name}\n")
    resumir_colunas(pasta_app)
    resumir_choices(pasta_app)


if __name__ == "__main__":
    main()