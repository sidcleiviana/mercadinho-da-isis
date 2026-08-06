from django import forms


class CodigoBarrasForm(forms.Form):
    codigo_barras = forms.CharField(
        label="Codigo de barras",
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "autofocus": "autofocus",
                "autocomplete": "off",
                "placeholder": "Aguardando codigo de barras...",
            }
        ),
    )
