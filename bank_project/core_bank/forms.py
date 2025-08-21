from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Service
from decimal import Decimal

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, help_text="Se autocompletará al ingresar el DNI.")
    last_name = forms.CharField(max_length=150, required=True, help_text="Se autocompletará al ingresar el DNI.")
    dni = forms.CharField(max_length=8, min_length=8, required=True, help_text="Ingresa tu DNI de 8 dígitos.")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'username',
            'email',
            'dni',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo dígitos.")
        if CustomUser.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Este DNI ya está registrado.")
        return dni

    def save(self, commit=True):
        user = super().save(commit=False)
        user.dni = self.cleaned_data['dni']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    # Personaliza el formulario de login si es necesario, por ejemplo, añadiendo clases CSS
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario o Email', 'class': 'input input-bordered w-full'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'input input-bordered w-full'}))


class TransferForm(forms.Form):
    recipient_identifier = forms.CharField(
        max_length=100,
        label="DNI o Nombre de Usuario del Destinatario",
        help_text="Ingresa el DNI o nombre de usuario del destinatario.",
        widget=forms.TextInput(attrs={'placeholder': 'DNI o Usuario', 'class': 'input input-bordered w-full'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        label="Monto a Transferir",
        widget=forms.NumberInput(attrs={'placeholder': 'Ej. 100.50', 'class': 'input input-bordered w-full'})
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        label="Descripción (opcional)",
        widget=forms.TextInput(attrs={'placeholder': 'Cena, alquiler, etc.', 'class': 'input input-bordered w-full'})
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("El monto debe ser mayor que cero.")
        return amount

class ServicePaymentForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        label="Selecciona el Servicio",
        empty_label="-- Seleccionar --",
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        label="Monto a Pagar",
        help_text="Ingresa el monto a pagar por el servicio.",
        widget=forms.NumberInput(attrs={'placeholder': 'Ej. 50.00', 'class': 'input input-bordered w-full'})
    )
    invoice_number = forms.CharField(
        max_length=50,
        required=False,
        label="Número de Factura/Recibo (opcional)",
        widget=forms.TextInput(attrs={'placeholder': '123456789', 'class': 'input input-bordered w-full'})
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("El monto debe ser mayor que cero.")
        return amount