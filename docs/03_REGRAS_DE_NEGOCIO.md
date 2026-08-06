# Regras de Negócio

**Documento:** 03_REGRAS_DE_NEGOCIO.md

---

# 1. Objetivo

Este documento define todas as regras de funcionamento do supermercado.

As regras descritas aqui possuem prioridade sobre qualquer decisão de implementação.

Nenhuma funcionalidade deverá contrariar estas regras.

---

# 2. O Mercado

O sistema representa um único supermercado.

Existe apenas:

* um mercado;
* um estoque;
* um caixa.

Não existem filiais.

Não existem múltiplos caixas.

Não existem múltiplos estoques.

---

# 3. Produtos

Todos os produtos devem ser cadastrados manualmente.

Cada produto obrigatoriamente possui:

* nome;
* foto;
* código de barras;
* preço;
* categoria.

Produtos não cadastrados não podem ser vendidos.

O código de barras deve ser único.

---

# 4. Cadastro de Estoque

Cadastrar um produto não significa possuir estoque.

Ao criar um produto, sua quantidade inicial será zero.

O estoque deverá ser abastecido posteriormente.

---

# 5. Entrada de Estoque

Sempre que novos produtos físicos forem colocados no mercado, o usuário deverá registrar a entrada manualmente.

O sistema nunca adiciona produtos automaticamente.

Toda entrada gera:

* aumento da quantidade;
* movimentação de estoque.

A entrada de estoque não altera automaticamente o caixa.

Caso a compra represente um gasto do mercado, deverá existir uma saída financeira separada.

---

# 6. Venda

Uma venda somente poderá ser concluída quando:

* existir pelo menos um item;
* todos os produtos possuírem estoque suficiente.

Ao concluir uma venda, o sistema deverá obrigatoriamente:

1. registrar a venda;
2. registrar todos os itens;
3. reduzir o estoque;
4. registrar movimentação de estoque;
5. registrar entrada no caixa.

Caso qualquer etapa falhe, toda a venda deverá ser cancelada.

---

# 7. Código de Barras

O leitor de código de barras funciona como um teclado.

Sempre que um código for recebido:

1. localizar o produto;
2. verificar existência;
3. verificar disponibilidade;
4. adicionar ao atendimento.

Caso o código não exista:

O sistema deverá informar claramente que o produto não foi encontrado.

Nenhuma venda poderá continuar utilizando um produto inexistente.

---

# 8. Estoque

O estoque nunca poderá possuir quantidade negativa.

Caso um produto esteja esgotado:

* ele continuará cadastrado;
* continuará aparecendo no sistema;
* não poderá ser vendido.

---

# 9. Caixa

Existe apenas um caixa.

Todo dinheiro do supermercado pertence ao caixa.

Entradas aumentam o saldo.

Saídas diminuem o saldo.

O saldo nunca deverá ser alterado manualmente sem geração de movimentação.

---

# 10. Compra de Estoque

Quando o usuário comprar novos produtos no mundo real, deverá registrar essa operação.

Essa operação é composta por duas ações independentes:

1. adicionar produtos ao estoque;
2. registrar a saída de dinheiro do caixa.

O sistema não deverá assumir automaticamente que uma entrada de estoque representa uma movimentação financeira.

---

# 11. Clientes Reais

Clientes reais são pessoas presentes fisicamente.

O sistema não exige cadastro.

A venda acontece normalmente.

O tipo da venda deverá ser registrado como:

Cliente Real.

---

# 12. Clientes Virtuais

Clientes virtuais existem apenas para complementar a brincadeira.

Eles não substituem clientes reais.

Não possuem personalidade.

Não possuem memória.

Não aprendem.

Não possuem relacionamento entre si.

São apenas nomes utilizados para representar atendimentos automáticos.

---

# 13. Quantidade de Clientes Virtuais

Ao iniciar um novo dia de funcionamento do mercado, o sistema deverá gerar automaticamente uma quantidade de atendimentos virtuais.

O número poderá ser configurável.

Valor padrão sugerido:

Entre 8 e 15 clientes.

Cada atendimento utiliza um cliente da lista disponível.

Um mesmo cliente virtual não deverá aparecer duas vezes no mesmo dia.

No dia seguinte todos voltam a estar disponíveis.

---

# 14. Horários

Cada cliente virtual recebe um horário aleatório de chegada.

Esse horário não é exibido ao usuário.

Quando o horário é atingido:

Uma notificação deverá aparecer informando que existe um cliente aguardando atendimento.

---

# 15. Fila

Caso vários clientes cheguem próximos entre si:

Eles deverão formar uma fila.

O usuário escolhe qual atender primeiro.

---

# 16. Tempo de Espera

Clientes virtuais aguardam atendimento por tempo limitado.

Caso não sejam atendidos:

O atendimento muda para:

Desistiu.

Nenhuma venda será realizada.

Nenhum produto será movimentado.

Nenhum dinheiro entrará no caixa.

---

# 17. Atendimento

Todo atendimento virtual acontece através de uma conversa guiada.

O usuário nunca digita texto livre.

Sempre responde utilizando opções apresentadas pelo sistema.

As respostas disponíveis dependem da etapa da conversa.

---

# 18. Produtos Solicitados

Cada atendimento possui um pedido próprio.

Os produtos solicitados são sorteados automaticamente.

A quantidade de itens poderá variar.

O cliente somente solicita produtos existentes no cadastro do sistema.

---

# 19. Produto Indisponível

Caso o produto solicitado não exista em estoque:

O usuário poderá informar que não possui o produto.

O cliente encerrará o atendimento.

A venda será cancelada.

Nenhum dinheiro entrará no caixa.

---

# 20. Venda Concluída

Quando todos os produtos forem separados corretamente:

O cliente realiza o pagamento automaticamente.

O sistema deverá:

* registrar a venda;
* reduzir o estoque;
* aumentar o caixa;
* finalizar o atendimento.

---

# 21. Relatórios

Todos os relatórios deverão ser calculados utilizando dados reais armazenados no banco.

Nenhum relatório poderá utilizar valores aproximados.

---

# 22. Integridade

Nenhuma operação poderá deixar o sistema em estado inconsistente.

Exemplos proibidos:

* vender sem reduzir estoque;
* vender sem registrar caixa;
* alterar estoque sem movimentação;
* alterar caixa sem movimentação.

---

# 23. Histórico

O sistema deverá preservar o histórico de:

* vendas;
* movimentações financeiras;
* movimentações de estoque;
* atendimentos virtuais.

Nenhuma dessas informações deverá ser perdida.

---

# 24. Exclusões

Sempre que possível utilizar:

* ativo;
* cancelado;
* inativo.

Evitar exclusão definitiva de registros.

---

# 25. Princípio Geral

Sempre que existir dúvida sobre o comportamento do sistema, deverá prevalecer a regra de que o supermercado deve funcionar da forma mais próxima possível de um pequeno mercado real, desde que essa complexidade continue adequada para uma criança.

O sistema deverá privilegiar simplicidade, previsibilidade e consistência em todas as operações.
