// ATENÇÃO: ao rodar, o ServiceNow cria permissões "cross scope" para o app.
// Antes de qualquer commit no Studio, apague-as (mantenha só o SysUserList).
// EN: creates invented test data (prefix "TESTE-") and runs architecture checks.
// Executar em System Definition > Scripts - Background, com o escopo do app selecionado.
// Todo o conteúdo é inventado: nada vem da wiki.
// Se já existirem dados TESTE-, rode antes limpar_dados_de_teste.js, porque a designação é única e uma segunda carga falharia por duplicidade.
(function executarCargaDeTeste() {
    var PREFIXO = 'x_1902920_scp_fo_0_';
    var TABELAS = {
        site: PREFIXO + 'foundation_site',
        registro: PREFIXO + 'scp_record',
        secao: PREFIXO + 'scp_section',
        midia: PREFIXO + 'scp_media'
    };
    var MARCADOR = 'TESTE-';

    // Ajuste (ou comente) o que quiser variar nessa execução, dá pra só colocar como false.
    var CONFIG = {
        criar: {
            site: true,
            registroCompleto: true,
            registroOutraLicenca: true,
            secoes: true,
            midias: true
        },
        testes: {
            padroes: true,
            regraDeNegocio: true,
            unico: true,
            cascata: true,
            restricao: true,
            conteudoOriginal: true
        }
    };

    function registrar(mensagem) {
        gs.info('[Carga de teste] ' + mensagem);
    }

    function verificar(nome, ok) {
        registrar((ok ? 'PASSOU  ' : 'FALHOU  ') + nome);
    }

    // Insere um registro ignorando campos vazios ou inexistentes. Devolve o sys_id (ou null).
    function inserir(tabela, campos) {
        var gr = new GlideRecord(tabela);
        gr.initialize();
        Object.keys(campos).forEach(function (nome) {
            var valor = campos[nome];
            if (valor === '' || valor === null || valor === undefined) return;
            if (!gr.isValidField(nome)) {
                registrar('campo ignorado (não existe): ' + tabela + '.' + nome);
                return;
            }
            gr.setValue(nome, valor);
        });
        var id = gr.insert();
        if (!id) registrar('a inserção não retornou registro em ' + tabela);
        return id;
    }

    // Devolve o valor de uma coluna do primeiro registro em que campo = valor.
    function obterValor(tabela, campo, valor, coluna) {
        var gr = new GlideRecord(tabela);
        return gr.get(campo, valor) ? gr.getValue(coluna) : null;
    }

    function contar(tabela, campo, valor) {
        var ga = new GlideAggregate(tabela);
        ga.addQuery(campo, valor);
        ga.addAggregate('COUNT');
        ga.query();
        return ga.next() ? parseInt(ga.getAggregate('COUNT'), 10) : 0;
    }

    function criarMassaDeTeste() {
        var ids = {};

        if (CONFIG.criar.site) {
            ids.site = inserir(TABELAS.site, {
                site_designation: MARCADOR + 'Site-01',
                site_type: 'research_facility',
                status: 'active',
                region: 'Região inventada para teste',
                site_director: gs.getUserID()
            });
        }

        if (CONFIG.criar.registroCompleto) {
            ids.completo = inserir(TABELAS.registro, {
                scp_designation: MARCADOR + '001',
                scp_number: 9001,
                title: 'Registro de teste com todos os campos preenchidos',
                object_class: 'euclid',
                description: '<p>Descrição inventada para os testes de arquitetura.</p>',
                special_containment_procedures: '<p>Procedimento de contenção inventado.</p>',
                original_content: '<p>Conteúdo original inventado.</p>',
                source_url: 'https://example.com/teste/001',
                author: 'Autor de Teste',
                text_license: 'cc_by_sa_3_0',
                review_status: 'imported',
                lead_researcher: gs.getUserID(),
                site_location: ids.site
            });
        }

        if (CONFIG.criar.registroOutraLicenca) {
            ids.outraLicenca = inserir(TABELAS.registro, {
                scp_designation: MARCADOR + '002',
                scp_number: 9002,
                title: 'Registro de teste com licença diferente do padrão',
                source_url: 'https://example.com/teste/002',
                text_license: 'other',
                license_details: 'Nota de licença inventada para o teste'
            });
        }

        if (CONFIG.criar.secoes && ids.completo) {
            [
                { rotulo: 'Adendo 1', tipo: 'addendum', ordem: 10, titulo: 'Primeiro adendo' },
                { rotulo: '2.1.3', tipo: 'interview', ordem: 20, titulo: 'Entrevista com um sujeito de teste' },
                { rotulo: 'Log A', tipo: 'exploration_log', ordem: 30, titulo: 'Log de exploração' }
            ].forEach(function (secao) {
                inserir(TABELAS.secao, {
                    scp_record: ids.completo,
                    section_type: secao.tipo,
                    order: secao.ordem,
                    section_label: secao.rotulo,
                    title: secao.titulo,
                    content: '<p>Texto de seção inventado.</p>'
                });
            });
        }

        if (CONFIG.criar.midias && ids.completo) {
            [
                { tipo: 'image', url: 'https://example.com/teste/imagem.png', legenda: 'Imagem de teste', status: 'pending' },
                { tipo: 'audio', url: 'https://example.com/teste/audio.mp3', legenda: 'Áudio de teste', status: 'verified' }
            ].forEach(function (midia) {
                inserir(TABELAS.midia, {
                    scp_record: ids.completo,
                    media_type: midia.tipo,
                    url: midia.url,
                    caption: midia.legenda,
                    author: 'Autor de Teste',
                    license: 'CC BY-SA 3.0',
                    verification_status: midia.status
                });
            });
        }

        return ids;
    }

    function executarTestes() {
        var t = CONFIG.testes;

        if (t.padroes) {
            inserir(TABELAS.registro, {
                scp_designation: MARCADOR + 'PADROES',
                title: 'Verificação de valores padrão',
                source_url: 'https://example.com/teste/padroes'
            });
            verificar('review_status padrão é imported',
                obterValor(TABELAS.registro, 'scp_designation', MARCADOR + 'PADROES', 'review_status') === 'imported');
            verificar('text_license padrão é cc_by_sa_3_0',
                obterValor(TABELAS.registro, 'scp_designation', MARCADOR + 'PADROES', 'text_license') === 'cc_by_sa_3_0');
        }

        if (t.regraDeNegocio) {
            // Caminho 1: registro já criado com licença Other.
            if (CONFIG.criar.registroOutraLicenca) {
                verificar('regra de negócio: needs_review ao criar com licença Other',
                    obterValor(TABELAS.registro, 'scp_designation', MARCADOR + '002', 'review_status') === 'needs_review');
            }

            // Caminho 2: troca de licença depois de criado (o uso real).
            var idRegra = inserir(TABELAS.registro, {
                scp_designation: MARCADOR + 'REGRA',
                title: 'Verificação da regra de negócio',
                source_url: 'https://example.com/teste/regra'
            });
            var gr = new GlideRecord(TABELAS.registro);
            gr.get(idRegra);
            gr.setValue('review_status', 'reviewed');
            gr.update();
            gr.setValue('text_license', 'other');
            gr.setValue('license_details', 'Nota de licença inventada');
            gr.update();
            verificar('regra de negócio: needs_review ao trocar a licença para Other',
                obterValor(TABELAS.registro, 'scp_designation', MARCADOR + 'REGRA', 'review_status') === 'needs_review');
        }

        if (t.unico) {
            var duplicado = inserir(TABELAS.registro, {
                scp_designation: MARCADOR + 'PADROES',
                title: 'Designação duplicada',
                source_url: 'https://example.com/teste/duplicado'
            });
            verificar('designação duplicada é rejeitada (Unique)', !duplicado);
        }

        if (t.cascata) {
            var idPai = inserir(TABELAS.registro, {
                scp_designation: MARCADOR + 'CASCATA',
                title: 'Verificação da cascata',
                source_url: 'https://example.com/teste/cascata'
            });
            inserir(TABELAS.secao, { scp_record: idPai, section_type: 'other', title: 'Seção filha' });
            inserir(TABELAS.midia, {
                scp_record: idPai,
                media_type: 'other',
                url: 'https://example.com/teste/filha',
                verification_status: 'pending'
            });
            var pai = new GlideRecord(TABELAS.registro);
            pai.get(idPai);
            pai.deleteRecord();
            verificar('apagar o registro apaga as seções', contar(TABELAS.secao, 'scp_record', idPai) === 0);
            verificar('apagar o registro apaga as mídias', contar(TABELAS.midia, 'scp_record', idPai) === 0);
        }

        if (t.restricao) {
            var idSite = inserir(TABELAS.site, { site_designation: MARCADOR + 'Site-R' });
            inserir(TABELAS.registro, {
                scp_designation: MARCADOR + 'RESTRICAO',
                title: 'Verificação da restrição',
                source_url: 'https://example.com/teste/restricao',
                site_location: idSite
            });
            var apagar = new GlideRecord(TABELAS.site);
            apagar.get(idSite);
            apagar.deleteRecord();
            var restante = new GlideRecord(TABELAS.site);
            verificar('site com SCPs alocados não pode ser apagado (Restrict)', restante.get(idSite));
        }

        if (t.conteudoOriginal && CONFIG.criar.registroCompleto) {
            var conteudo = obterValor(TABELAS.registro, 'scp_designation', MARCADOR + '001', 'original_content');
            verificar('script consegue gravar Original Content (somente leitura no formulário)',
                !!conteudo && conteudo.length > 0);
        }
    
    }
    try {
        var ids = criarMassaDeTeste();
        executarTestes();
        registrar('concluído');
    } catch (erro) {
        registrar('ERRO: ' + erro);
    }
    
})();