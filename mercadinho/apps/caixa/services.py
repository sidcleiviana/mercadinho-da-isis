from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from .models import Caixa, MovimentacaoFinanceira


def obter_caixa():
    caixa, _ = Caixa.objects.get_or_create(
        pk=1,
        defaults={"saldo_atual": Decimal("0.00")},
    )
    return caixa


def calcular_saldo():
    entradas = (
        MovimentacaoFinanceira.objects.filter(
            tipo=MovimentacaoFinanceira.Tipo.ENTRADA
        ).aggregate(total=Sum("valor"))["total"]
        or Decimal("0.00")
    )
    saidas = (
        MovimentacaoFinanceira.objects.filter(
            tipo=MovimentacaoFinanceira.Tipo.SAIDA
        ).aggregate(total=Sum("valor"))["total"]
        or Decimal("0.00")
    )
    return entradas - saidas


def sincronizar_saldo_caixa():
    caixa = obter_caixa()
    caixa.saldo_atual = calcular_saldo()
    caixa._permitir_atualizar_saldo = True
    caixa.save(update_fields=["saldo_atual", "atualizado_em"])
    return caixa


def registrar_movimentacao_financeira(tipo, valor, descricao, venda=None):
    if valor <= Decimal("0"):
        raise ValidationError("O valor deve ser maior que zero.")
    if not descricao or not descricao.strip():
        raise ValidationError("Informe uma descricao.")
    if tipo not in MovimentacaoFinanceira.Tipo.values:
        raise ValidationError("Tipo de movimentacao financeira invalido.")

    with transaction.atomic():
        caixa = Caixa.objects.select_for_update().get(pk=obter_caixa().pk)
        saldo_atual = calcular_saldo()
        if tipo == MovimentacaoFinanceira.Tipo.SAIDA and valor > saldo_atual:
            raise ValidationError("O caixa nao possui saldo suficiente para esta saida.")

        movimentacao = MovimentacaoFinanceira.objects.create(
            tipo=tipo,
            valor=valor,
            descricao=descricao.strip(),
            data=timezone.now(),
            venda=venda,
        )
        caixa.saldo_atual = calcular_saldo()
        caixa._permitir_atualizar_saldo = True
        caixa.save(update_fields=["saldo_atual", "atualizado_em"])

    return caixa, movimentacao
