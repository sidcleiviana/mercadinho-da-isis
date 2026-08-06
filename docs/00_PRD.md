# PRD - Mercadinho Infantil

**Projeto:** Mercadinho Da Ísis
**Versão:** 1.0
**Status:** Em desenvolvimento

---

# 1. Objetivo

Desenvolver um sistema web que simule a operação de um pequeno supermercado para uso infantil.

O objetivo principal não é criar um jogo, mas sim uma experiência de aprendizagem baseada em uma brincadeira realista.

O sistema deverá ensinar, de forma natural, conceitos como:

* organização;
* atendimento ao cliente;
* controle de estoque;
* fluxo de caixa;
* registro de vendas;
* tomada de decisões simples.

Todas as funcionalidades devem existir para tornar a brincadeira mais próxima da operação de um supermercado real.

---

# 2. Filosofia do Projeto

Este projeto **não é um jogo**.

O sistema não deve possuir elementos tradicionais de gamificação.

Não devem existir:

* níveis;
* experiência (XP);
* medalhas;
* missões;
* recompensas diárias;
* moedas especiais;
* sistemas de energia;
* desbloqueios artificiais;
* qualquer mecanismo criado apenas para prender a atenção do usuário.

Sempre que existir uma decisão entre:

> parecer um jogo

ou

> parecer um supermercado,

a implementação deverá escolher a segunda opção.

---

# 3. Público-alvo

O sistema foi desenvolvido para ser utilizado principalmente por crianças.

A interface deverá ser simples, intuitiva e visual.

Mesmo sabendo ler, crianças tendem a reconhecer imagens mais rapidamente do que texto.

Sempre que possível, utilizar:

* fotografias dos produtos;
* botões grandes;
* poucos elementos na tela;
* linguagem simples;
* organização clara.

---

# 4. Tecnologia

## Backend

* Django

## Banco de dados

* SQLite

## Frontend

* HTML
* CSS
* JavaScript

O projeto deverá utilizar prioritariamente recursos nativos do Django.

Evitar dependências desnecessárias.

---

# 5. Persistência

Todas as informações do sistema deverão permanecer salvas entre as execuções.

O sistema nunca deverá perder dados após ser fechado.

Deverão ser persistidos:

* produtos;
* estoque;
* caixa;
* histórico de vendas;
* clientes virtuais atendidos;
* configurações;
* imagens cadastradas.

---

# 6. Estrutura Geral

O sistema será dividido nos seguintes módulos:

* Produtos
* Estoque
* Caixa
* Vendas
* Clientes Virtuais
* Relatórios
* Administração

Cada módulo deverá ser independente, porém integrado aos demais.

---

# 7. Princípios de Desenvolvimento

Todo o projeto deverá seguir os seguintes princípios:

* código limpo;
* arquitetura modular;
* responsabilidade única;
* baixo acoplamento;
* alta legibilidade;
* reutilização de componentes;
* nomenclatura clara;
* tipagem sempre que possível;
* utilização do ORM do Django;
* separação entre regras de negócio e interface.

Evitar duplicação de código.

---

# 8. Princípios da Interface

A interface deverá transmitir a sensação de um sistema profissional simplificado.

Não utilizar:

* animações exageradas;
* efeitos chamativos;
* excesso de cores;
* elementos que distraiam a criança.

O foco deverá permanecer sempre na operação do supermercado.

---

# 9. Experiência do Usuário

Ao utilizar o sistema, a criança deve sentir que administra um mercado verdadeiro.

Todas as ações deverão produzir consequências reais dentro do sistema.

Exemplos:

* vender um produto reduz o estoque;
* vender um produto aumenta o caixa;
* comprar estoque aumenta a quantidade disponível;
* comprar estoque reduz o saldo do caixa.

O sistema deverá incentivar a organização através das próprias regras do mercado, e nunca através de recompensas artificiais.

---

# 10. Realismo

Embora seja destinado ao público infantil, o comportamento interno do sistema deverá ser consistente.

Todas as operações deverão respeitar regras de negócio.

Exemplos:

* não é possível vender um produto inexistente;
* não é possível vender quantidade superior ao estoque;
* o caixa deve refletir todas as movimentações financeiras;
* relatórios devem representar exatamente os dados registrados.

---

# 11. Escalabilidade

O projeto deverá ser desenvolvido pensando em crescimento.

Novos módulos poderão ser adicionados futuramente sem necessidade de reescrever a arquitetura existente.

Toda implementação deverá favorecer manutenção simples e expansão futura.

---

# 12. Papel da Inteligência Artificial durante o Desenvolvimento

Toda IA utilizada para desenvolver este projeto deverá atuar como um engenheiro de software sênior.

A IA não deve criar funcionalidades por iniciativa própria.

Sempre deverá seguir rigorosamente esta documentação.

Caso exista conflito entre implementação e documentação, a documentação possui prioridade.

Caso alguma regra de negócio esteja ausente, a IA deverá propor uma solução antes de implementá-la.

---

# 13. Objetivo Final

Ao finalizar o desenvolvimento, o sistema deverá permitir que uma criança utilize um computador ou tablet para administrar um pequeno supermercado, realizando vendas para clientes reais e clientes virtuais, utilizando produtos físicos identificados por código de barras, mantendo controle de estoque, registrando movimentações financeiras no caixa e consultando relatórios, tudo de forma simples, intuitiva e próxima da realidade.

O sucesso do projeto não será medido pela quantidade de funcionalidades, mas pela capacidade de proporcionar uma experiência natural, educativa e divertida sem depender de mecanismos artificiais de gamificação.
