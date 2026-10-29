import re
from collections import Counter

from dados import iterar_registros

# O sentido de "site" aqui é de "instalações", facilities.
PADRAO_SITE = re.compile(r"\bSite[- ]?(\d{1,3})\b", re.IGNORECASE)

contagem_sites = Counter()
com_site = 0
total = 0

for designacao, registro in iterar_registros():
    total += 1
    html = registro.get("raw_content") or ""
    sites = set(PADRAO_SITE.findall(html))
    if sites:
        com_site += 1
        contagem_sites.update(sites)

print(f"Registros analisados: {total}")
print(f"Com alguma menção a Site-N: {com_site}")
print(f"Sem menção: {total - com_site}")
print("\nSites mais citados (nº de registros):")
for numero, qtd in contagem_sites.most_common(10):
    print(f"  Site-{numero}: {qtd}")