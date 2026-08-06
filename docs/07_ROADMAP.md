# Roadmap de Desenvolvimento

**Documento:** 07_ROADMAP.md

---

# 1. Objetivo

Este documento define a ordem oficial de implementação do sistema.

A sequência foi planejada para minimizar retrabalho, reduzir dependências entre módulos e garantir que cada etapa seja construída sobre uma base sólida.

Nenhuma etapa deverá iniciar antes da conclusão da etapa anterior, salvo justificativa técnica.

---

# 2. Princípios

Cada etapa deve resultar em um sistema funcional.

Mesmo incompleto, o projeto deverá permanecer executável ao final de cada fase.

Sempre que possível:

* implementar;
* testar;
* validar;
* somente então iniciar a próxima etapa.

---

# 3. Etapa 1 — Estrutura Inicial

Objetivo:

Criar toda a base do projeto.

Itens:

* criar projeto Django;
* configurar SQLite;
* configurar estrutura de Apps;
* configurar arquivos estáticos;
* configurar pasta media;
* configurar autenticação;
* configurar painel administrativo;
* configurar layout base.

Resultado esperado:

Projeto executando corretamente.

---

# 4. Etapa 2 — Banco de Dados

Objetivo:

Criar todos os Models.

Itens:

* Produto;
* Categoria;
* Estoque;
* Movimentação de Estoque;
* Caixa;
* Movimentação Financeira;
* Venda;
* ItemVenda;
* Atendimento Virtual;
* Configurações.

Resultado esperado:

Banco completamente estruturado.

---

# 5. Etapa 3 — Cadastro de Produtos

Objetivo:

Permitir cadastrar produtos.

Itens:

* formulário;
* upload de foto;
* categoria;
* código de barras;
* preço;
* pesquisa;
* edição.

Resultado esperado:

Produtos totalmente funcionais.

---

# 6. Etapa 4 — Estoque

Objetivo:

Controlar quantidade disponível.

Itens:

* entrada manual;
* consulta;
* movimentações;
* validações.

Resultado esperado:

Controle completo do estoque.

---

# 7. Etapa 5 — Caixa

Objetivo:

Controlar movimentações financeiras.

Itens:

* saldo;
* entradas;
* saídas;
* histórico.

Resultado esperado:

Caixa operacional.

---

# 8. Etapa 6 — Sistema de Vendas

Objetivo:

Implementar o funcionamento do caixa.

Itens:

* leitura de código de barras;
* carrinho;
* cálculo automático;
* finalização;
* integração com estoque;
* integração com caixa.

Resultado esperado:

Venda completa funcionando.

---

# 9. Etapa 7 — Dashboard

Objetivo:

Criar a tela principal.

Itens:

* resumo do mercado;
* saldo do caixa;
* estoque;
* notificações;
* botão Iniciar Expediente;
* botão Encerrar Expediente.

Resultado esperado:

Dashboard operacional.

---

# 10. Etapa 8 — Motor de Clientes Virtuais

Objetivo:

Criar o mecanismo de geração de atendimentos.

Itens:

* geração diária;
* horários aleatórios;
* fila;
* desistência;
* histórico.

Resultado esperado:

Clientes chegando automaticamente.

---

# 11. Etapa 9 — Central de Atendimento

Objetivo:

Criar o ambiente de atendimento.

Itens:

* fila;
* abertura do atendimento;
* lista de produtos;
* estados do atendimento.

Resultado esperado:

Atendimentos funcionando.

---

# 12. Etapa 10 — Conversa Guiada

Objetivo:

Implementar o fluxo de conversa.

Itens:

* mensagens;
* botões;
* validações;
* integração com vendas.

Resultado esperado:

Conversas completas.

---

# 13. Etapa 11 — Relatórios

Objetivo:

Gerar informações administrativas.

Itens:

* vendas;
* caixa;
* estoque;
* clientes;
* resumo diário.

Resultado esperado:

Relatórios completos.

---

# 14. Etapa 12 — Interface

Objetivo:

Refinar toda a experiência do usuário.

Itens:

* responsividade;
* animações discretas;
* ícones;
* organização visual;
* melhorias de usabilidade.

Resultado esperado:

Sistema agradável e intuitivo.

---

# 15. Etapa 13 — Testes

Objetivo:

Garantir estabilidade.

Itens:

* testes unitários;
* testes de integração;
* validação de fluxos;
* correção de inconsistências.

Resultado esperado:

Sistema confiável.

---

# 16. Etapa 14 — Revisão Final

Objetivo:

Preparar a primeira versão oficial.

Itens:

* revisão geral;
* limpeza do código;
* documentação;
* otimizações;
* revisão visual.

Resultado esperado:

Versão 1.0 concluída.

---

# 17. Regras de Implementação

Durante todo o desenvolvimento:

* nunca pular etapas;
* nunca criar funcionalidades sem documentação;
* nunca duplicar lógica;
* sempre reutilizar componentes existentes;
* sempre respeitar a arquitetura definida.

---

# 18. Critério de Conclusão

Uma etapa somente poderá ser considerada concluída quando:

* toda funcionalidade estiver implementada;
* todos os testes passarem;
* nenhuma inconsistência conhecida permanecer;
* a documentação estiver atualizada.

Somente então a próxima etapa poderá ser iniciada.

---

# 19. Objetivo Final

Ao concluir todas as etapas deste roadmap, o sistema deverá representar um supermercado funcional, consistente, educativo e preparado para futuras evoluções, mantendo fidelidade às especificações definidas nos demais documentos desta pasta.
