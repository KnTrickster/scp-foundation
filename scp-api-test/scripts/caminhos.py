from pathlib import Path

# scripts/ -> scp-api-test/
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "data"
PASTA_RELATORIOS = PASTA_PROJETO / "reports"

ARQUIVO_INDICE = PASTA_DADOS / "index.json"
ARQUIVO_CONTEUDO = PASTA_DADOS / "content_series-1.json"
ARQUIVO_TITULOS = PASTA_DADOS / "titulos_serie1.json"