from decimal import Decimal

from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["foto", "nome", "categoria", "codigo_barras", "preco_venda", "ativo"]
        labels = {
            "foto": "Foto",
            "nome": "Nome",
            "categoria": "Categoria",
            "codigo_barras": "Codigo de barras",
            "preco_venda": "Preco",
            "ativo": "Ativo",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome do produto"}),
            "codigo_barras": forms.TextInput(attrs={"placeholder": "Codigo de barras"}),
            "preco_venda": forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.foto:
            self.fields["foto"].required = False

    def clean_preco_venda(self):
        preco_venda = self.cleaned_data["preco_venda"]
        if preco_venda <= Decimal("0"):
            raise forms.ValidationError("O preco deve ser maior que zero.")
        return preco_venda

    def clean_foto(self):
        foto = self.cleaned_data.get("foto")
        if not foto and not (self.instance and self.instance.pk and self.instance.foto):
            raise forms.ValidationError("A foto do produto e obrigatoria.")
        return foto
