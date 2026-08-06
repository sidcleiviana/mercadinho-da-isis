from django.shortcuts import render

from .services import (
    relatorio_caixa,
    relatorio_clientes,
    relatorio_estoque,
    relatorio_geral,
    relatorio_vendas,
)


def resumo(request):
    return render(request, "relatorios/resumo.html", relatorio_geral())


def vendas(request):
    return render(
        request,
        "relatorios/vendas.html",
        {"relatorio": relatorio_vendas()},
    )


def caixa(request):
    return render(
        request,
        "relatorios/caixa.html",
        {"relatorio": relatorio_caixa()},
    )


def estoque(request):
    return render(
        request,
        "relatorios/estoque.html",
        {"relatorio": relatorio_estoque()},
    )


def clientes(request):
    return render(
        request,
        "relatorios/clientes.html",
        {"relatorio": relatorio_clientes()},
    )
