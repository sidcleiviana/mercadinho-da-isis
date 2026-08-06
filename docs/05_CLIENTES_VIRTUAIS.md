# Motor de Clientes Virtuais

**Documento:** 05_CLIENTES_VIRTUAIS.md

---

# 1. Objetivo

O Motor de Clientes Virtuais é responsável por gerar atendimentos automáticos durante o funcionamento do mercado.

Seu objetivo é manter o supermercado em funcionamento mesmo quando não existem clientes reais presentes.

Os clientes virtuais não substituem clientes reais.

Eles apenas simulam consumidores entrando no mercado para realizar compras.

---

# 2. Filosofia

Os clientes virtuais não são personagens.

Eles não possuem:

* personalidade;
* memória;
* humor;
* preferências;
* evolução;
* relacionamento.

São apenas nomes utilizados para identificar cada atendimento.

O foco sempre será a venda.

Nunca a interação social.

---

# 3. Lista de Clientes

O sistema possuirá uma lista fixa de clientes.

Exemplo:

* Ana
* Carlos
* Fernanda
* João
* Julia
* Lucas
* Maria
* Pedro
* Rafael
* Sofia
* Helena
* Miguel
* Laura
* Gustavo
* Beatriz

A lista poderá ser alterada pelo administrador.

---

# 4. Mercado Aberto

Os clientes virtuais somente existem quando o mercado estiver aberto.

Ao abrir o mercado:

O sistema deverá iniciar um novo dia de funcionamento.

Nesse momento serão gerados todos os atendimentos do dia.

Enquanto o mercado estiver fechado:

Nenhum cliente poderá surgir.

---

# 5. Quantidade Diária

No início do dia o sistema deverá definir automaticamente quantos atendimentos existirão.

Valor padrão:

Entre 8 e 15.

Esse valor poderá ser configurado futuramente.

---

# 6. Seleção dos Clientes

Cada atendimento utiliza um cliente da lista.

Durante um mesmo dia:

Um cliente não poderá aparecer duas vezes.

No dia seguinte todos voltam a ficar disponíveis.

---

# 7. Horários

Cada atendimento recebe um horário aleatório.

O horário pertence ao intervalo entre:

Abertura do mercado

e

Fechamento do mercado.

Esses horários não deverão ser exibidos ao usuário.

---

# 8. Chegada

Quando chegar o horário programado:

O cliente entra na fila automaticamente.

Uma notificação deverá ser exibida imediatamente.

Exemplo:

Novo cliente aguardando atendimento.

---

# 9. Fila

Caso existam vários clientes aguardando:

Todos permanecerão na fila.

O usuário escolhe quem atender primeiro.

A fila deverá mostrar:

* Nome
* Horário de chegada
* Tempo aguardando

---

# 10. Tempo Máximo

Cada cliente possui um tempo máximo de espera.

Caso esse tempo seja ultrapassado:

O cliente abandona a fila.

O atendimento muda para:

Desistiu.

Nenhuma venda acontece.

---

# 11. Atendimento

Ao iniciar o atendimento:

O cliente deixa a fila.

O atendimento passa para:

Em Atendimento.

Nenhum outro usuário poderá atender o mesmo cliente simultaneamente.

---

# 12. Estrutura da Conversa

Toda conversa segue um fluxo pré-definido.

Nunca utilizar inteligência artificial.

Nunca utilizar geração automática de texto.

Nunca permitir digitação livre.

Todas as mensagens são controladas pelo sistema.

---

# 13. Respostas

O usuário responde apenas utilizando botões.

Exemplos:

Sim

Não

Adicionar Produto

Finalizar Venda

Cancelar Atendimento

As opções disponíveis variam conforme o momento da conversa.

---

# 14. Pedido

Cada cliente possui um pedido gerado automaticamente.

O pedido contém:

* um ou mais produtos;
* quantidade desejada.

Os produtos são sorteados apenas entre aqueles cadastrados e ativos.

---

# 15. Produtos Indisponíveis

Caso um produto solicitado não exista em estoque:

O usuário poderá informar essa situação.

O cliente encerrará a compra.

O atendimento será finalizado sem venda.

---

# 16. Venda

Quando todos os produtos forem registrados corretamente:

O cliente realiza o pagamento automaticamente.

O sistema deverá:

* concluir a venda;
* atualizar estoque;
* atualizar caixa;
* registrar o atendimento.

---

# 17. Cancelamento

O usuário poderá cancelar um atendimento.

Nesse caso:

O cliente será considerado desistente.

Nenhuma venda será registrada.

---

# 18. Final do Dia

Ao fechar o mercado:

Todos os atendimentos ainda aguardando deverão ser encerrados automaticamente.

Seu status será:

Não Atendido.

Nenhum novo cliente será criado até que o mercado seja aberto novamente.

---

# 19. Histórico

Cada atendimento deverá permanecer registrado.

Informações mínimas:

* cliente;
* horário de chegada;
* início do atendimento;
* fim do atendimento;
* duração;
* status;
* valor vendido.

---

# 20. Estatísticas

O sistema deverá ser capaz de calcular:

* quantidade de clientes atendidos;
* quantidade de desistências;
* tempo médio de espera;
* tempo médio de atendimento;
* faturamento dos clientes virtuais.

---

# 21. Independência

O Motor de Clientes Virtuais deverá funcionar independentemente da interface.

A interface apenas apresenta as informações.

Toda a lógica deverá permanecer no backend.

---

# 22. Determinismo

Todo atendimento deverá seguir regras previsíveis.

Nunca utilizar comportamentos imprevisíveis baseados em inteligência artificial.

O mesmo fluxo deverá sempre produzir os mesmos resultados.

---

# 23. Escalabilidade

O motor deverá permitir futuramente:

* diferentes tipos de pedidos;
* promoções;
* horários especiais;
* dias com maior movimento;
* eventos sazonais.

Essas funcionalidades não fazem parte da primeira versão.

A arquitetura apenas deverá permitir sua implementação futura.

---

# 24. Objetivo

O Motor de Clientes Virtuais deverá criar a sensação de um supermercado em funcionamento, mantendo um fluxo natural de clientes ao longo do dia, sem transformar a experiência em um jogo ou em uma simulação baseada em personagens.
