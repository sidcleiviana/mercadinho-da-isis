# Cenário: Cliente Desiste

## Contexto
Cliente virtual aguardando atendimento na fila.

---

## Sequência

10:02 — Cliente "João" entra na fila.

10:03 — Nenhum atendimento iniciado.

10:08 — Tempo máximo de espera atingido.

Sistema:

- Altera status do atendimento para "Desistiu"
- Remove cliente da fila

---

## Mensagem

"João foi embora. Tempo de espera excedido."

---

## Estado do Sistema

- Cliente: desistente
- Caixa: inalterado
- Estoque: inalterado
- Venda: não criada

---

## Resultado

Nenhuma operação financeira ocorreu.
Nenhuma movimentação de estoque ocorreu.