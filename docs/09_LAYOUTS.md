# Layouts da Interface

**Documento:** 09_LAYOUTS.md

---

# 1. Objetivo

Este documento define a organização visual das telas do sistema.

Não define cores nem identidade visual (isso pertence ao Design System).

Define apenas:

* disposição dos componentes;
* comportamento das telas;
* fluxo de navegação;
* hierarquia visual.

Todas as telas deverão seguir estas especificações.

---

# 2. Filosofia

O usuário principal é uma criança.

Portanto toda tela deverá responder rapidamente três perguntas:

* Onde eu estou?
* O que posso fazer?
* O que aconteceu?

A interface nunca deverá gerar dúvida.

---

# 3. Estrutura Geral

Todas as telas (exceto o Modo Atendimento) seguem esta estrutura:

```
+-----------------------------------------------------------+
| Logo         Nome do Mercado           Hora      Usuário  |
+-----------------------------------------------------------+

| Menu |                                             |
|      |                                             |
|      |             Conteúdo Principal              |
|      |                                             |
|      |                                             |
|      |                                             |
|      |                                             |

+-----------------------------------------------------------+
| Status do Sistema                                         |
+-----------------------------------------------------------+
```

---

# 4. Menu Lateral

Sempre fixo.

Itens:

🏠 Dashboard

🛒 Produtos

📦 Estoque

💰 Caixa

👥 Atendimento

📊 Relatórios

⚙ Configurações

O menu nunca desaparece.

Exceto durante um atendimento.

---

# 5. Dashboard

É a tela inicial.

Objetivo:

Mostrar rapidamente o estado do supermercado.

Wireframe:

```
+----------------------------------------------------+

Mercadinho da Alice

Expediente: FECHADO

[ INICIAR EXPEDIENTE ]

------------------------------------------------------

Caixa Atual

R$ 148,50

------------------------------------------------------

Produtos em Estoque

152

------------------------------------------------------

Clientes aguardando

0

------------------------------------------------------

Resumo do Último Dia

Clientes Atendidos

Clientes Perdidos

Valor Vendido

------------------------------------------------------
```

Quando o expediente estiver aberto:

O botão muda para:

**ENCERRAR EXPEDIENTE**

---

# 6. Notificações

As notificações aparecem no canto superior direito.

Exemplo:

```
Novo cliente aguardando atendimento.
```

Ao clicar:

Abrir Central de Atendimento.

As notificações desaparecem automaticamente após alguns segundos.

---

# 7. Tela de Produtos

Objetivo:

Consultar produtos.

Wireframe:

```
Pesquisar:

[________________________]

------------------------------------------------

Foto

Arroz

R$ 29,90

Categoria

Alimentos

------------------------------------------------

Foto

Leite

R$ 5,50

Categoria

Bebidas

------------------------------------------------

[ Novo Produto ]
```

Cada produto possui botão:

Editar

---

# 8. Cadastro de Produto

Wireframe:

```
Foto

[Selecionar Arquivo]

Nome

[________________]

Categoria

[v]

Código de Barras

[________________]

Preço

[________]

[Salvar]

[Cancelar]
```

---

# 9. Estoque

Objetivo:

Consultar quantidade.

Wireframe:

```
Pesquisar

[________________]

------------------------------------------------

Foto

Arroz

Quantidade

15

[Adicionar Estoque]

------------------------------------------------

Foto

Leite

Quantidade

8

[Adicionar Estoque]
```

Ao clicar em "Adicionar Estoque":

Abrir modal.

```
Quantidade

[____]

[Confirmar]

[Cancelar]
```

---

# 10. Caixa

Wireframe:

```
Saldo Atual

R$ 342,80

-----------------------------------------

Entradas

Venda #153

+ R$ 18,00

-----------------------------------------

Saídas

Reposição de Estoque

- R$ 45,00

-----------------------------------------

[Registrar Saída]
```

---

# 11. Registrar Saída

Modal

```
Valor

[_______]

Descrição

[____________________]

[Salvar]

[Cancelar]
```

---

# 12. Central de Atendimento

Esta tela mostra todos os atendimentos.

```
Clientes aguardando

--------------------------------------------------

Ana

Chegou há 2 minutos

[Atender]

--------------------------------------------------

Carlos

Chegou há 30 segundos

[Atender]

--------------------------------------------------

João

Chegou há 5 minutos

[Atender]
```

Nenhuma conversa acontece nesta tela.

Ela serve apenas para organizar a fila.

---

# 13. Modo Atendimento

Esta é a principal tela do sistema.

Quando aberta:

Todo o restante da interface desaparece.

Não existe menu.

Não existe dashboard.

Não existe navegação.

A criança sente que está sentada no caixa do mercado.

Wireframe:

```
+--------------------------------------------------------------+

Cliente

Maria

---------------------------------------------------------------

CHAT

Olá!

Gostaria de comprar dois pacotes de arroz.

---------------------------------------------------------------

RESPONDER

[Tenho]

[Não tenho]

---------------------------------------------------------------

Produtos solicitados

✔ Arroz x2

---------------------------------------------------------------

Leitura dos Produtos

(Aguardando código de barras...)

---------------------------------------------------------------

Produtos registrados

Arroz

Arroz

---------------------------------------------------------------

TOTAL

R$ 59,80

---------------------------------------------------------------

[Finalizar Venda]
```

Após concluir:

Retornar automaticamente para a Central de Atendimento.

---

# 14. Produto Lido

Sempre que um código de barras for reconhecido:

Exibir rapidamente:

```
✔ Produto Encontrado

Foto

Arroz

R$ 29,90
```

Após alguns segundos:

Ocultar automaticamente.

---

# 15. Código Não Encontrado

Exibir:

```
❌ Produto não encontrado.

Tente novamente.
```

Nenhuma ação adicional.

---

# 16. Cliente Desiste

Caso ultrapasse o tempo máximo:

Mostrar:

```
João foi embora.

Tempo de espera excedido.
```

A mensagem desaparece automaticamente.

---

# 17. Relatórios

Wireframe

```
Hoje

---------------------------------

Vendas

18

---------------------------------

Faturamento

R$ 428,90

---------------------------------

Clientes Atendidos

14

---------------------------------

Clientes Perdidos

2

---------------------------------

Produto Mais Vendido

Arroz
```

Gráficos simples.

Poucos elementos.

---

# 18. Configurações

Wireframe

```
Nome do Mercado

[________________]

Quantidade Máxima de Clientes

[15]

Tempo Máximo de Espera

[10 minutos]

Hora de Início

[08:00]

Hora de Encerramento

[18:00]

[Salvar]
```

---

# 19. Resumo do Expediente

Ao encerrar o expediente:

Exibir uma tela exclusiva.

```
Expediente Encerrado

Clientes Atendidos

12

Clientes Perdidos

2

Valor Vendido

R$ 386,40

Saldo Atual

R$ 1.248,50

Produto Mais Vendido

Leite

[Voltar ao Dashboard]
```

Esta tela é apenas informativa.

---

# 20. Navegação

Fluxo principal:

```
Dashboard

↓

Iniciar Expediente

↓

Clientes começam a chegar

↓

Central de Atendimento

↓

Modo Atendimento

↓

Central de Atendimento

↓

Dashboard

↓

Encerrar Expediente

↓

Resumo do Expediente

↓

Dashboard
```

---

# 21. Regra de Ouro

O usuário nunca deverá precisar pensar onde clicar.

Em qualquer tela, a próxima ação esperada deve estar evidente.

A interface deve transmitir tranquilidade, organização e controle, permitindo que a criança concentre sua atenção na brincadeira de administrar um pequeno supermercado.
