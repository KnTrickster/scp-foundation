from dados import iterar_registros

tamanhos = sorted(
    ((len(r.get("raw_content") or ""), d) for d, r in iterar_registros()),
    reverse=True,
)
for tamanho, designacao in tamanhos[:10]:
    print(f"{designacao}: {tamanho} caracteres")