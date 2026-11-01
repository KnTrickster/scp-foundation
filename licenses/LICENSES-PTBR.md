# Licenciamento e atribuição

Este projeto é uma aplicação desenvolvida na plataforma ServiceNow, inspirada no universo da SCP Foundation. Trata-se de um projeto independente, criado para fins de aprendizado e composição de portfólio (consulte a seção 7).

## 1. Conteúdo da SCP Wiki

O universo SCP é escrito e mantido por uma comunidade de autores. O conteúdo da Wiki é licenciado sob a [Creative Commons Atribuição-CompartilhaIgual 3.0 (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/), de acordo com as condições descritas pela própria Wiki.

- **Fonte:** [SCP Foundation Wiki](https://scp-wiki.wikidot.com/)
- **Guia de licenciamento:** [Licensing Guide](https://scp-wiki.wikidot.com/licensing-guide)
- **Licença:** [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

As atribuições dos artigos, autores e recursos individuais são registradas nas seções abaixo. **Este repositório não contém o texto de nenhum artigo.** Os arquivos de dados brutos são intencionalmente excluídos (consulte [\`docs/decisions.md\`](../docs/decisions.md), decisão D12).

## 2. Origem dos dados

Os dados dos artigos foram obtidos por meio do projeto [scp-data](https://github.com/scp-data), um conjunto de dados construído a partir da coleta de informações da Wiki. A documentação do projeto informa que ele não possui vínculo com a SCP Wiki ou seus administradores e que todo o conteúdo da Wiki presente nele está sujeito à licença da própria Wiki. Portanto, os termos de licenciamento da Wiki também se aplicam aos dados.

Consulte [\`scp-api-test/data/README.md\`](../scp-api-test/data/README.md) para saber como obter os arquivos e qual versão do conjunto de dados foi utilizada.

## 3. Arquivos de dados derivados presentes neste repositório

| Arquivos | Conteúdo |
|---|---|
| \`scp-api-test/data/titulos_serie1.json\` | Identificações SCP e títulos utilizados no índice da Série 1 da Wiki |
| \`scp-api-test/reports/\*.csv\` | Identificações, títulos, URLs de páginas e mídias, nomes de arquivos de imagem, contagens e sinalizadores |

Nenhum desses arquivos contém textos de artigos. Esses arquivos são disponibilizados sob a licença CC BY-SA 3.0, com atribuição à SCP Wiki e ao projeto scp-data.

## 4. Recursos visuais

Cada recurso externo é documentado individualmente.

| Recurso | Arquivo | Autor | Fonte | Licença | Modificações |
|---|---|---|---|---|---|
| Logotipo da SCP Foundation | \`system-images/logos/SCP_Foundation_(emblem).svg\` | far2 / Aelanna | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:SCP_Foundation_(emblem).svg) | CC BY-SA 3.0 | Nenhuma |
| Redesign do SCP-173 | \`system-images/scp-records/scp-173_grimbuscula.png\` | [@Grimbuscula](https://x.com/Grimbuscula) | [Galeria de redesigns do SCP-173](https://scp-wiki.wikidot.com/scp-173-redesign-collab-hub-subpage-4) | CC BY-SA 3.0 | Nenhuma |

Recursos cuja autoria ou licença ainda não tenham sido confirmadas não são incluídos no repositório.

**Capturas de tela.** As imagens presentes em \`system-images/system-screenshots/\` mostram a aplicação ServiceNow e podem conter textos ou imagens da Wiki. Cada uma delas possui os devidos créditos em sua legenda.

## 5. Obras utilizadas

Uma entrada para cada artigo utilizado.

| Título | Autor | URL original | Licença | Utilização | Modificações |
|---|---|---|---|---|---|
| SCP-173 | Moto42 | [https://scp-wiki.wikidot.com/scp-173](https://scp-wiki.wikidot.com/scp-173) | CC BY-SA 3.0 | Reprodução em uma instância privada do ServiceNow, para fins de estudo. Não faz parte deste repositório | Nenhuma |

Quando o texto de um artigo é importado, cada registro contém seus próprios campos \`Author\`, \`Source URL\` e \`Text License\` (consulte [\`docs/decisions.md\`](../docs/decisions.md), decisão D6).

## 6. Código e contribuições originais

O código, a estrutura técnica e a documentação desenvolvidos para este projeto são identificados separadamente dos materiais de terceiros e dos conteúdos derivados do universo SCP.

Eles são licenciados sob a [Licença MIT](../LICENSE). A Licença MIT **não** abrange o conteúdo da Wiki, os arquivos de dados derivados mencionados na seção 3 ou os recursos de terceiros mencionados na seção 4, que permanecem sujeitos às respectivas licenças indicadas acima.

<!-- Após entrar em contato com a equipe de licenciamento da Wiki, adicionar aqui a data e quaisquer orientações recebidas. -->

## 7. Independência

Este é um projeto independente, desenvolvido para fins de aprendizado e composição de portfólio. Não se trata de um produto oficial da SCP Foundation Wiki e não implica aprovação ou patrocínio por parte de seus autores ou colaboradores. ServiceNow é uma marca registrada da ServiceNow, Inc.; este projeto não possui vínculo com a empresa nem é endossado por ela.

---

*Este documento é atualizado sempre que novas fontes, recursos ou contribuições são adicionados.*