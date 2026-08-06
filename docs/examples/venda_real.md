# Cenário: Venda Real

## Contexto
Cliente real está sendo atendido no modo atendimento.

---

## Sequência

09:12 — Cliente "Carlos" inicia atendimento.

09:13 — Cliente solicita:
- 2 Arroz
- 1 Leite

09:14 — Criança passa os produtos no leitor de código de barras.

Sistema:

- Identifica "Arroz"
- Identifica "Leite"

- Adiciona itens ao atendimento

---

## Cálculo

Arroz: R$ 29,90 x 2 = R$ 59,80  
Leite: R$ 5,50 x 1 = R$ 5,50  

Total: R$ 65,30

---

## Finalização

09:15 — Cliente realiza pagamento automático.

Sistema executa:

- Cria registro de Venda
- Cria Itens da Venda
- Atualiza Estoque (-2 Arroz, -1 Leite)
- Registra Movimentação de Estoque
- Registra Entrada no Caixa (+R$ 65,30)

---

## Estado Final

- Caixa: aumenta
- Estoque: reduzido
- Atendimento: finalizado
- Cliente: concluído