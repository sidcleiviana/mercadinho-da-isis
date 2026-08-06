# Banco de Dados

**Documento:** 02_DATABASE.md

---

# 1. Objetivo

Este documento define todas as entidades persistentes do sistema.

O objetivo é garantir consistência dos dados e evitar duplicidade de informações.

O banco de dados deverá ser implementado utilizando SQLite através do ORM do Django.

---

# 2. Princípios Gerais

Todo dado persistente deverá possuir uma única fonte de verdade.

Evitar duplicação de informações.

Sempre que possível utilizar relacionamentos entre entidades.

Todo Model deverá possuir:

* identificador único;
* data de criação;
* data de atualização.

Esses campos poderão ser implementados através de uma classe base reutilizável.

---

# 3. Produto

Representa um produto físico existente no supermercado.

Campos obrigatórios:

* Nome
* Código de Barras
* Preço de Venda
* Foto
* Categoria
* Ativo (Sim/Não)

Regras:

* O código de barras deve ser único.
* Produtos inativos não poderão ser vendidos.
* A foto será utilizada em toda a interface.
* O preço vigente será utilizado durante a venda.

---

# 4. Categoria

Organiza os produtos.

Campos:

* Nome
* Cor (opcional)
* Ordem de exibição

Exemplos:

* Alimentos
* Bebidas
* Limpeza
* Higiene
* Doces

---

# 5. Estoque

Representa a quantidade disponível de um produto.

Campos:

* Produto
* Quantidade Atual

Regras:

Cada produto possui exatamente um registro de estoque.

Nunca existirão dois estoques para o mesmo produto.

Quantidade nunca poderá ser negativa.

---

# 6. Movimentação de Estoque

Toda alteração de quantidade deverá gerar uma movimentação.

Campos:

* Produto
* Tipo
* Quantidade
* Data
* Observação

Tipos possíveis:

* Entrada
* Venda
* Ajuste Manual

Objetivo:

Permitir auditoria completa do estoque.

Nenhuma alteração deverá ocorrer sem registro.

---

# 7. Caixa

Representa o caixa único do supermercado.

Campos:

* Saldo Atual

Regras:

Existe apenas um caixa.

Todo dinheiro do supermercado pertence ao caixa.

O saldo nunca deverá ser alterado diretamente.

Sempre através de movimentações.

---

# 8. Movimentação do Caixa

Representa qualquer entrada ou saída financeira.

Campos:

* Tipo
* Valor
* Descrição
* Data

Tipos:

* Venda
* Compra de Estoque
* Ajuste Manual

Regras:

O saldo do caixa deverá ser calculado automaticamente a partir das movimentações ou atualizado de forma transacional pela lógica de negócio.

Nunca permitir alteração manual do saldo sem registrar movimentação.

---

# 9. Venda

Representa uma venda concluída.

Campos:

* Número da Venda
* Data
* Tipo de Cliente
* Valor Total
* Status

Tipo de Cliente:

* Real
* Virtual

Status:

* Concluída
* Cancelada

---

# 10. Item da Venda

Representa cada produto vendido.

Campos:

* Venda
* Produto
* Quantidade
* Valor Unitário
* Valor Total

Regras:

Uma venda possui um ou mais itens.

Cada item pertence a apenas uma venda.

O valor unitário deverá ser armazenado na venda.

Mudanças futuras no preço do produto não alteram vendas antigas.

---

# 11. Cliente Virtual

Representa um nome disponível para geração automática de atendimentos.

Campos:

* Nome
* Ativo

Regras:

Os clientes não possuem personalidade.

Não possuem preferências.

Não possuem histórico comportamental.

São apenas identificadores utilizados durante os atendimentos.

A lista inicial deverá conter aproximadamente quinze nomes.

Novos nomes poderão ser adicionados futuramente.

---

# 12. Atendimento Virtual

Representa um atendimento gerado automaticamente.

Campos:

* Cliente Virtual
* Horário Programado
* Horário de Início
* Horário de Finalização
* Status
* Valor Total

Status possíveis:

* Aguardando
* Em Atendimento
* Finalizado
* Desistiu

Cada atendimento representa um pedido independente.

Mesmo cliente poderá aparecer novamente em outro dia.

---

# 13. Pedido Virtual

Representa os produtos desejados pelo cliente virtual.

Campos:

* Atendimento
* Produto
* Quantidade

Regras:

Os produtos são sorteados automaticamente.

O cliente não possui memória de compras anteriores.

Cada atendimento gera um novo pedido.

---

# 14. Configuração

Armazena parâmetros do sistema.

Campos sugeridos:

* Nome do Mercado
* Quantidade Máxima de Clientes Virtuais por Dia
* Tempo Máximo de Espera
* Horário de Abertura
* Horário de Fechamento

Todas as configurações deverão ficar centralizadas nesta entidade.

---

# 15. Relacionamentos

Categoria

↓

Produto

↓

Estoque

↓

Movimentações de Estoque

---

Produto

↓

Itens da Venda

↓

Venda

↓

Movimentações do Caixa

---

Cliente Virtual

↓

Atendimento

↓

Pedido

---

# 16. Exclusões

Evitar exclusão física de registros.

Sempre que possível utilizar:

* Ativo
* Cancelado
* Inativo

O histórico nunca deverá ser perdido.

---

# 17. Integridade

Toda venda concluída deverá obrigatoriamente:

1. Registrar a venda.
2. Registrar os itens vendidos.
3. Reduzir o estoque.
4. Registrar movimentação de estoque.
5. Registrar movimentação financeira.
6. Atualizar o saldo do caixa.

Caso qualquer etapa falhe, toda a operação deverá ser cancelada.

A operação deverá ocorrer dentro de uma transação do banco de dados.

---

# 18. Auditoria

O banco deverá permitir reconstruir toda a operação do supermercado.

Através dos registros armazenados deverá ser possível descobrir:

* quais produtos existiam em determinado dia;
* quanto havia em estoque;
* quanto havia no caixa;
* quais vendas foram realizadas;
* quais produtos foram vendidos;
* quais clientes virtuais foram atendidos;
* quais atendimentos foram perdidos.

Nenhuma informação necessária para auditoria deverá ser descartada.

---

# 19. Escalabilidade

O modelo de dados deverá permitir futuras implementações como:

* fornecedores;
* compras de mercadorias;
* múltiplos caixas;
* múltiplos usuários;
* impressão de comprovantes;
* integração com leitores e impressoras.

Essas funcionalidades não fazem parte da primeira versão, porém o banco deverá permitir sua evolução sem necessidade de remodelagem completa.

---

# 20. Fonte de Verdade

O banco de dados é a única fonte oficial de informação do sistema.

Nenhuma regra de negócio deverá depender exclusivamente de variáveis temporárias, sessões ou dados armazenados apenas em memória.

Todas as operações relevantes deverão ser persistidas imediatamente.
