# Cenário: Chegada de Cliente

## Contexto
O mercado está com o expediente aberto. O sistema já gerou os atendimentos do dia.

---

## Sequência

08:03 — O expediente está ativo.

08:07 — O sistema identifica que um atendimento programado atingiu seu horário.

08:07 — Cliente "Ana" é liberada para entrada na fila.

Sistema:

- Cria notificação:
  "Novo cliente aguardando atendimento."

- Adiciona Ana na Central de Atendimento.

---

## Estado do Sistema

- Mercado: ABERTO
- Fila: 1 cliente (Ana)
- Caixa: R$ 0,00 (sem vendas ainda)
- Estoque: inalterado
- Atendimento: aguardando início

---

## Resultado

O cliente está disponível para ser atendido.
A criança pode iniciar o atendimento quando desejar.

## Regras Técnicas

- Este fluxo não pode ser assíncrono sem controle de estado
- Toda mudança deve ser persistida no banco
- Nenhum cliente pode ser gerado fora do expediente