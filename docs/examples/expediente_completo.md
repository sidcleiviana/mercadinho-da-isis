# Cenário: Expediente Completo

## Contexto
Dia completo de operação do mercado.

---

## Início

08:00 — Criança inicia expediente.

Sistema:

- Gera 12 atendimentos virtuais
- Distribui horários ao longo do dia
- Ativa fila de clientes

---

## Durante o Dia

08:10 — Cliente Ana atendido  
08:25 — Cliente Carlos atendido  
09:00 — Cliente Maria desistiu  
10:15 — Cliente João atendido  
11:40 — Cliente Helena atendido  

Vendas são registradas continuamente.

Estoque é atualizado automaticamente.

Caixa acumula valores.

---

## Encerramento

17:58 — Último cliente atendido.

18:00 — Criança encerra expediente.

---

## Processamento Final

Sistema calcula:

- Total de vendas: 14
- Clientes atendidos: 11
- Clientes desistentes: 3
- Faturamento: R$ 486,20

---

## Atualizações

- Caixa atualizado com total do dia
- Nenhuma venda pendente
- Nenhum atendimento ativo

---

## Resumo Exibido

"Expediente encerrado com sucesso."

---

## Estado Final

- Mercado: FECHADO
- Caixa: atualizado
- Estoque: atualizado
- Atendimentos: finalizados