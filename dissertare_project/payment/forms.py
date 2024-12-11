""" payment forms """
from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    place_choice = [
        ("Enviar", "Enviar"),
        ("Recolher na loja", "Recolher na loja")
    ]

    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}), required=True)
    shipping_email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}), required=True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço 1'}), required=True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço 2'}), required=False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}), required=True)
    shipping_phone_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de telefone'}), required=True)
    shipping_mode = forms.ChoiceField(label="", choices=place_choice, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_mode', 'shipping_full_name', 'shipping_email', 'shipping_phone_number', 'shipping_address1', 'shipping_address2', 'shipping_city']

        exclude = ['user',]


class PaymentForm(forms.Form):
    payment_options = [
        ("TPA - Terminal de Pagamento Automático", "TPA - Terminal de Pagamento Automático"),
        ("CASH - DINHEIRO VIVO", "CASH - DINHEIRO VIVO"),
        ("Transferência Bancária", "Transferência Bancária"),
        ("Multicaixa Express", "Multicaixa Express")
    ]
    
    payment_mode = forms.ChoiceField(label="", choices=payment_options, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), required=True)
