// ATENÇÃO: ao rodar, o ServiceNow cria permissões "cross scope" para o app.
// Antes de qualquer commit no Studio, apague-as (mantenha só o SysUserList).
// EN: removes the invented test data created by gerar_dados_de_teste.js (prefix "TESTE-").
// Executar em System Definition > Scripts - Background, com o escopo do app selecionado.
(function limparDadosDeTeste() {
    var PREFIXO = 'x_1902920_scp_fo_0_';
    var MARCADOR = 'TESTE-';
    var SIMULAR = false; // true = só lista o que seria removido, sem apagar nada

    function registrar(mensagem) {
        gs.info('[Limpeza de teste] ' + mensagem);
    }

    function removerOnde(tabela, campo) {
        var gr = new GlideRecord(tabela);
        gr.addQuery(campo, 'STARTSWITH', MARCADOR);
        gr.query();
        var encontrados = 0;
        var removidos = 0;
        while (gr.next()) {
            encontrados++;
            registrar((SIMULAR ? 'seria removido: ' : 'removendo: ') + gr.getValue(campo));
            if (!SIMULAR && gr.deleteRecord()) removidos++;
        }
        registrar(tabela + ': encontrados = ' + encontrados + ', removidos = ' + removidos);
    }

    // Registros primeiro: as seções e mídias saem junto, pela cascata.
    // Sites depois, porque a regra Restrict impede apagar um site que ainda tem SCPs.
    removerOnde(PREFIXO + 'scp_record', 'scp_designation');
    removerOnde(PREFIXO + 'foundation_site', 'site_designation');
    registrar('concluído');
})();