# Cenário: Produto Sem Estoque

## Contexto
Durante um atendimento ativo.

---

## Sequência

11:20 — Cliente solicita:
- Arroz

11:21 — Produto existe no sistema.

11:21 — Sistema verifica estoque:

Resultado: 0 unidades disponíveis

---

## Resposta do Sistema

"Produto indisponível."

---

## Decisão do Usuário

A criança informa ao cliente que o produto não está disponível.

Cliente reage:

- encerra o atendimento

---

## Consequência

Sistema executa:

- Cancela atendimento
- Não cria venda
- Não movimenta estoque
- Não movimenta caixa

---

## Estado Final

- Venda: não realizada
- Caixa: inalterado
- Estoque: inalterado
- Atendimento: encerrado (cancelado)