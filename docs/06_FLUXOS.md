# Fluxos do Sistema

**Documento:** 06_FLUXOS.md

---

# 1. Objetivo

Este documento descreve o fluxo operacional completo do supermercado.

Cada fluxo representa uma sequência de ações realizadas pelo usuário e pelo sistema.

Os fluxos aqui definidos possuem prioridade sobre decisões de implementação.

---

# 2. Fluxo Geral

O funcionamento do sistema segue sempre esta sequência:

Mercado Fechado

↓

Abrir Mercado

↓

Chegada de Clientes

↓

Atendimento

↓

Venda

↓

Atualização de Estoque

↓

Atualização do Caixa

↓

Próximo Cliente

↓

Fechar Mercado

↓

Resumo do Dia

---

# 3. Abrir Mercado

Usuário acessa o Dashboard.

↓

Pressiona:

**Abrir Mercado**

↓

Sistema cria um novo dia de operação.

↓

Sistema sorteia os atendimentos do dia.

↓

Sistema define horários aleatórios de chegada.

↓

Sistema inicia o relógio interno.

↓

Mercado passa para:

**Aberto**

---

# 4. Chegada de Cliente

Chega o horário programado.

↓

Sistema cria uma notificação.

↓

Cliente entra na fila.

↓

Dashboard atualiza automaticamente.

↓

Central de Atendimento mostra novo atendimento aguardando.

---

# 5. Atendimento

Usuário seleciona:

**Atender**

↓

Sistema abre o Modo Atendimento.

↓

Toda a interface passa a exibir apenas:

* conversa;
* pedido;
* leitura dos produtos;
* total da compra.

Menus ficam ocultos durante todo o atendimento.

---

# 6. Conversa

Cliente inicia a conversa.

↓

Sistema apresenta opções de resposta.

↓

Usuário responde utilizando botões.

↓

Sistema avança para a próxima etapa da conversa.

Nenhuma digitação é utilizada.

---

# 7. Separação dos Produtos

Cliente informa os produtos desejados.

↓

Usuário pega os produtos físicos.

↓

Passa cada produto no leitor.

↓

Sistema identifica o código.

↓

Localiza o produto.

↓

Adiciona automaticamente ao atendimento.

↓

Atualiza o valor parcial.

↓

Repete até concluir todos os itens.

---

# 8. Produto Não Encontrado

Caso o código de barras não exista:

Sistema informa:

Produto não encontrado.

↓

Nenhum item é adicionado.

↓

Usuário poderá tentar novamente.

---

# 9. Produto Sem Estoque

Caso o produto esteja sem estoque:

Sistema informa:

Produto indisponível.

↓

Usuário poderá responder ao cliente que o produto não está disponível.

↓

Cliente encerra o atendimento.

↓

Nenhuma venda será realizada.

---

# 10. Finalização da Venda

Todos os produtos foram registrados.

↓

Sistema calcula o valor total.

↓

Cliente realiza pagamento automaticamente.

↓

Sistema registra:

* venda;
* itens;
* movimentação de estoque;
* movimentação financeira.

↓

Atendimento é encerrado.

↓

Sistema retorna automaticamente para a Central de Atendimento.

---

# 11. Cliente Desiste

Cliente permanece aguardando além do tempo permitido.

↓

Sistema altera o status para:

Desistiu.

↓

Cliente deixa a fila.

↓

Nenhuma movimentação financeira ocorre.

---

# 12. Entrada de Estoque

Usuário acessa:

Estoque.

↓

Seleciona um produto.

↓

Escolhe:

Adicionar Estoque.

↓

Informa quantidade.

↓

Sistema aumenta o estoque.

↓

Sistema registra movimentação.

---

# 13. Saída Financeira

Usuário acessa:

Caixa.

↓

Seleciona:

Registrar Saída.

↓

Informa:

* valor;
* descrição.

↓

Sistema reduz saldo.

↓

Sistema registra movimentação.

---

# 14. Cadastro de Produto

Administrador acessa:

Produtos.

↓

Novo Produto.

↓

Preenche:

* foto;
* nome;
* categoria;
* código de barras;
* preço.

↓

Salvar.

↓

Produto fica disponível para uso.

↓

Quantidade inicial:

Zero.

---

# 15. Consulta de Estoque

Usuário abre:

Estoque.

↓

Sistema apresenta:

* foto;
* nome;
* quantidade.

↓

Usuário pode localizar rapidamente qualquer produto.

---

# 16. Consulta do Caixa

Usuário abre:

Caixa.

↓

Sistema apresenta:

Saldo Atual.

↓

Entradas.

↓

Saídas.

↓

Histórico.

---

# 17. Relatórios

Usuário abre:

Relatórios.

↓

Sistema calcula em tempo real:

* vendas;
* faturamento;
* estoque;
* clientes atendidos;
* clientes desistentes.

Nenhum relatório utiliza valores estimados.

---

# 18. Fechar Mercado

Usuário pressiona:

Fechar Mercado.

↓

Sistema impede novas chegadas.

↓

Atendimentos pendentes são encerrados.

↓

Sistema calcula estatísticas do dia.

↓

Resumo é apresentado.

↓

Mercado passa para:

Fechado.

---

# 19. Resumo do Dia

Ao fechar o mercado deverá ser apresentado um painel contendo:

* total de vendas;
* faturamento;
* saldo atual do caixa;
* clientes atendidos;
* clientes desistentes;
* produtos mais vendidos;
* movimentações do estoque.

O usuário poderá apenas visualizar essas informações.

Nenhuma alteração poderá ser feita nesta tela.

---

# 20. Fluxo de Erros

Sempre que ocorrer uma falha, o sistema deverá:

* informar claramente o problema;
* impedir operações inconsistentes;
* manter todos os dados íntegros.

Jamais deixar o usuário em dúvida sobre o estado atual da operação.

---

# 21. Fluxo da Interface

Fluxo padrão:

Dashboard

↓

Central de Atendimento

↓

Modo Atendimento

↓

Central de Atendimento

↓

Dashboard

O usuário nunca deverá navegar para outras telas enquanto um atendimento estiver em andamento.

---

# 22. Objetivo

Todos os fluxos do sistema deverão transmitir a sensação de operação contínua de um pequeno supermercado, com foco em simplicidade, organização e previsibilidade.

Cada ação realizada pelo usuário deverá produzir um resultado imediato, claro e consistente.
