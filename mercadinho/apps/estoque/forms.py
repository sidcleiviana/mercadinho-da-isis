from django import forms


class EntradaEstoqueForm(forms.Form):
    quantidade = forms.IntegerField(
        label="Quantidade",
        min_value=1,
        widget=forms.NumberInput(attrs={"min": "1", "step": "1"}),
    )
    observacao = forms.CharField(
        label="Observacao",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Observacao opcional"}),
    )
