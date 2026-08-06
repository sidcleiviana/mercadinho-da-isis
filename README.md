# Mercadinho da Ísis

Sistema web em Django que simula a operação de um supermercado real simplificado, com foco educativo e operacional.

## Funcionalidades

- Cadastro de produtos
- Controle de estoque
- Caixa e movimentações financeiras
- Vendas com baixa de estoque e entrada no caixa
- Clientes virtuais e central de atendimento
- Conversa guiada
- Relatórios gerenciais
- Interface responsiva com identidade visual própria

## Rodar localmente

```bash
cd mercadinho
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Depois acesse:

```text
http://127.0.0.1:8000
```

## Deploy

O projeto está preparado para deploy em serviços como Render.

Consulte [DEPLOY.md](DEPLOY.md).

## Documentação

Toda a especificação do produto está na pasta [docs](docs).
