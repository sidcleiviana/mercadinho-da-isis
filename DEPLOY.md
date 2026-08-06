# Deploy publico

Este projeto esta preparado para deploy em um provedor Python/Django, como Render.

## Render

1. Suba este repositorio para GitHub.
2. No Render, escolha **New > Blueprint**.
3. Aponte para o repositorio.
4. O Render usara `render.yaml`.
5. Ao final, ajuste se necessario:
   - `ALLOWED_HOSTS`
   - `CSRF_TRUSTED_ORIGINS`

## Variaveis obrigatorias

- `DEBUG=False`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`

## Comandos de validacao

```bash
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```
