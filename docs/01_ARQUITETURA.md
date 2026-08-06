# Arquitetura do Sistema

**Documento:** 01_ARQUITETURA.md

---

# 1. Objetivo

Este documento define a arquitetura de software do projeto.

Todas as implementações deverão seguir esta estrutura.

O objetivo é manter o sistema organizado, modular, fácil de manter e preparado para futuras expansões.

Nenhuma funcionalidade deverá ser implementada fora desta arquitetura sem justificativa técnica.

---

# 2. Tecnologias

## Backend

* Python 3.x
* Django

## Banco de Dados

* SQLite

## Frontend

* HTML5
* CSS3
* JavaScript

Utilizar prioritariamente recursos nativos do Django.

Evitar dependências externas sempre que possível.

---

# 3. Estrutura Geral do Projeto

O projeto deverá seguir uma arquitetura baseada em aplicações (Django Apps).

Cada módulo do sistema deverá possuir responsabilidades bem definidas.

Estrutura sugerida:

```
mercadinho/

│
├── apps/
│
│   ├── core/
│   ├── produtos/
│   ├── estoque/
│   ├── caixa/
│   ├── vendas/
│   ├── clientes/
│   ├── relatorios/
│   └── configuracoes/
│
├── docs/
│
├── media/
│
├── static/
│
├── templates/
│
├── manage.py
│
└── requirements.txt
```

---

# 4. Responsabilidade de cada App

## Core

Responsável por:

* configurações gerais
* autenticação
* dashboard
* página inicial
* componentes compartilhados
* utilidades do sistema

Nenhuma regra de negócio específica deverá ficar neste módulo.

---

## Produtos

Responsável por:

* cadastro de produtos
* código de barras
* preço
* categoria
* foto
* pesquisa de produtos

Este módulo nunca altera estoque.

---

## Estoque

Responsável por:

* quantidade disponível
* entrada de produtos
* saída automática durante vendas
* histórico de movimentações
* conferência de estoque

Este módulo controla apenas quantidade.

Não controla dinheiro.

---

## Caixa

Responsável por:

* saldo atual
* entradas
* saídas
* histórico financeiro

O caixa representa todo o dinheiro disponível do supermercado.

Não existe módulo "Banco".

---

## Vendas

Responsável por:

* carrinho
* leitura do código de barras
* cálculo do total
* fechamento da venda
* geração dos registros financeiros
* comunicação entre caixa e estoque

Toda venda deverá passar obrigatoriamente por este módulo.

---

## Clientes

Responsável por:

* clientes virtuais
* fila de atendimento
* chat
* pedidos
* geração automática de clientes
* histórico de atendimentos

Clientes reais não precisam de cadastro obrigatório.

---

## Relatórios

Responsável por:

* vendas
* movimentações
* caixa
* estoque
* estatísticas

Nenhum dado deverá ser armazenado aqui.

Todos os relatórios deverão ser calculados a partir das informações existentes.

---

## Configurações

Responsável por:

* preferências do sistema
* parâmetros
* horários
* quantidade máxima de clientes
* demais configurações administrativas

---

# 5. Separação de Responsabilidades

Cada módulo deverá possuir apenas uma responsabilidade principal.

Exemplo:

Produtos conhecem:

* nome
* preço
* código de barras

Produtos NÃO conhecem:

* saldo do caixa
* vendas
* clientes

---

Estoque conhece:

* quantidade

Estoques NÃO conhecem:

* preço
* dinheiro
* clientes

---

Caixa conhece:

* entradas
* saídas
* saldo

Caixa NÃO conhece:

* quantidade de produtos

---

Essa separação deverá ser mantida durante todo o projeto.

---

# 6. ORM

Toda persistência deverá utilizar exclusivamente o ORM do Django.

Não utilizar SQL bruto, exceto quando absolutamente necessário e devidamente documentado.

---

# 7. Models

Cada entidade do sistema deverá possuir seu próprio Model.

Exemplos:

* Produto
* Categoria
* Caixa
* MovimentacaoCaixa
* Venda
* ItemVenda
* ClienteVirtual
* PedidoVirtual
* MovimentacaoEstoque

Evitar Models com responsabilidades múltiplas.

---

# 8. Views

As Views deverão ser leves.

Toda regra de negócio deverá ficar em serviços ou métodos específicos.

As Views devem apenas:

* receber requisições;
* validar entradas;
* chamar a lógica de negócio;
* retornar respostas.

---

# 9. Templates

Todos os templates deverão reutilizar componentes.

Evitar repetição.

Sempre utilizar:

* template base
* blocos
* includes

---

# 10. Arquivos Estáticos

Separar corretamente:

* CSS
* JavaScript
* imagens
* ícones

Nunca misturar lógica JavaScript dentro do HTML quando houver alternativa mais organizada.

---

# 11. Imagens

As imagens dos produtos deverão ser armazenadas na pasta media.

O banco de dados deverá armazenar apenas o caminho da imagem.

Nunca armazenar imagens diretamente no banco.

---

# 12. Código de Barras

O leitor deverá ser tratado como um teclado.

Sempre que um código for recebido:

1. localizar o produto;
2. validar existência;
3. validar disponibilidade;
4. executar a ação correspondente.

O sistema nunca deverá depender de hardware específico.

Qualquer leitor que funcione como teclado deverá ser compatível.

---

# 13. Comunicação entre módulos

Nenhum módulo deverá acessar diretamente o banco de outro módulo.

A comunicação deverá ocorrer através das regras de negócio.

Exemplo:

Venda concluída

↓

Vendas solicita atualização

↓

Estoque reduz quantidade

↓

Caixa registra entrada

↓

Relatórios passam a enxergar a nova venda

Cada módulo executa apenas sua própria responsabilidade.

---

# 14. Escalabilidade

A arquitetura deverá permitir futura implementação de:

* múltiplos caixas;
* vários usuários;
* fornecedores;
* compras;
* impressão de etiquetas;
* impressão de comprovantes;
* integração com impressoras térmicas;
* acesso remoto;
* aplicativo móvel.

Essas funcionalidades não fazem parte da primeira versão, porém a arquitetura não deverá impedir sua implementação futura.

---

# 15. Código

Todo código produzido deverá obedecer aos seguintes princípios:

* simples;
* legível;
* reutilizável;
* modular;
* documentado apenas quando necessário;
* sem duplicação de lógica.

Priorizar clareza ao invés de soluções excessivamente complexas.

---

# 16. Convenções

Utilizar nomenclatura consistente.

Classes:

```
Produto
Venda
ClienteVirtual
```

Métodos:

```
criar_venda()

registrar_pagamento()

adicionar_estoque()

finalizar_atendimento()
```

Variáveis devem possuir nomes descritivos.

Evitar abreviações desnecessárias.

---

# 17. Objetivo da Arquitetura

A arquitetura deste projeto deve permitir que qualquer desenvolvedor consiga localizar rapidamente cada responsabilidade do sistema.

Nenhum módulo deverá crescer de forma desorganizada.

A estrutura deve permanecer simples, previsível e consistente durante toda a evolução do projeto.
