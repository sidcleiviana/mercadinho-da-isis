from decimal import Decimal

from django import forms


class MovimentacaoFinanceiraForm(forms.Form):
    valor = forms.DecimalField(
        label="Valor",
        min_value=Decimal("0.01"),
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
    )
    descricao = forms.CharField(
        label="Descricao",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Descricao da movimentacao"}),
    )

    def clean_descricao(self):
        descricao = self.cleaned_data["descricao"].strip()
        if not descricao:
            raise forms.ValidationError("Informe uma descricao.")
        return descricao
