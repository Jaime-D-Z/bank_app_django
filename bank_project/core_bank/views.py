from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction as db_transaction
from django.contrib import messages
import requests
import os
from dotenv import load_dotenv
from decimal import Decimal

from .models import CustomUser, Transaction, Service, ServicePayment
from .forms import CustomUserCreationForm, UserLoginForm, TransferForm, ServicePaymentForm

load_dotenv()

DECOLECTA_API_TOKEN = os.getenv("DECOLECTA_API_TOKEN")

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Te hemos asignado un saldo inicial de S/10,000.00.")
            return redirect('core_bank:dashboard')
        else:
            if not os.getenv("DEBUG", "True").lower() == "true":
                print(f"Intento de registro fallido: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'core_bank/register.html', {'form': form})

def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido de nuevo, {user.first_name}!")
                return redirect('core_bank:dashboard')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
                if not os.getenv("DEBUG", "True").lower() == "true":
                    print(f"Intento de login fallido para el usuario: {username}")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('core_bank:login')

@login_required
def dashboard_view(request):
    user = request.user
    recent_transactions = Transaction.objects.filter(sender=user).order_by('-timestamp')[:5]
    recent_payments = ServicePayment.objects.filter(user=user).order_by('-timestamp')[:5]

    return render(request, 'core_bank/dashboard.html', {
        'user': user,
        'recent_transactions': recent_transactions,
        'recent_payments': recent_payments,
    })

@login_required
def transfer_view(request):
    user = request.user
    form = TransferForm()

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_identifier = form.cleaned_data['recipient_identifier']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']

            try:
                with db_transaction.atomic():
                    recipient = None
                    if recipient_identifier.isdigit() and len(recipient_identifier) == 8:
                        recipient = CustomUser.objects.filter(dni=recipient_identifier).first()
                    if not recipient:
                        recipient = CustomUser.objects.filter(username=recipient_identifier).first()

                    if not recipient:
                        messages.error(request, "Destinatario no encontrado. Verifica el DNI o nombre de usuario.")
                        return render(request, 'core_bank/transfer.html', {'form': form})

                    if user.id == recipient.id:
                        messages.error(request, "No puedes transferirte a ti mismo.")
                        return render(request, 'core_bank/transfer.html', {'form': form})

                    if user.balance < amount:
                        messages.error(request, "Saldo insuficiente para realizar esta transferencia.")
                        return render(request, 'core_bank/transfer.html', {'form': form})

                    user.balance -= amount
                    recipient.balance += amount
                    user.save()
                    recipient.save()

                    Transaction.objects.create(
                        sender=user,
                        receiver=recipient,
                        amount=amount,
                        transaction_type='transferencia',
                        description=description
                    )
                    messages.success(request, f"¡Transferencia de S/{amount} a {recipient.first_name} {recipient.last_name} ({recipient.username}) realizada con éxito!")
                    return redirect('core_bank:dashboard')

            except Exception as e:
                messages.error(request, f"Ocurrió un error al procesar la transferencia: {e}")
                if not os.getenv("DEBUG", "True").lower() == "true":
                    print(f"Error de transferencia: {e}")

    return render(request, 'core_bank/transfer.html', {'form': form})

@login_required
def services_view(request):
    services = Service.objects.all()
    form = ServicePaymentForm()

    if not services.exists():
        Service.objects.bulk_create([
            Service(name="Agua (SEDAPAL)"),
            Service(name="Luz (Luz del Sur)"),
            Service(name="Internet (Claro/Movistar)"),
            Service(name="Teléfono Fijo"),
            Service(name="Gas Natural"),
            Service(name="Arriendo"),
            Service(name="Tarjeta de Crédito (Visa)"),
            Service(name="Tarjeta de Crédito (Mastercard)"),
            Service(name="Educación (Colegio/Universidad)"),
            Service(name="Salud (Seguro/Clínica)"),
        ])
        services = Service.objects.all()

    if request.method == 'POST':
        form = ServicePaymentForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            amount = form.cleaned_data['amount']
            invoice_number = form.cleaned_data['invoice_number']
            user = request.user

            try:
                with db_transaction.atomic():
                    if user.balance < amount:
                        messages.error(request, "Saldo insuficiente para pagar este servicio.")
                        return render(request, 'core_bank/services.html', {'form': form, 'services': services})

                    user.balance -= amount
                    user.save()

                    ServicePayment.objects.create(
                        user=user,
                        service=service,
                        amount=amount,
                        invoice_number=invoice_number
                    )
                    Transaction.objects.create(
                        sender=user,
                        receiver=None,
                        amount=amount,
                        transaction_type='pago_servicio',
                        description=f"Pago de {service.name} (Factura: {invoice_number or 'N/A'})"
                    )

                    messages.success(request, f"¡Pago de S/{amount} para {service.name} realizado con éxito!")
                    return redirect('core_bank:dashboard')

            except Exception as e:
                messages.error(request, f"Ocurrió un error al procesar el pago: {e}")
                if not os.getenv("DEBUG", "True").lower() == "true":
                    print(f"Error de pago de servicio: {e}")

    return render(request, 'core_bank/services.html', {'form': form, 'services': services})


@login_required
def history_view(request):
    user = request.user
    transactions = Transaction.objects.filter(sender=user).order_by('-timestamp')
    payments = ServicePayment.objects.filter(user=user).order_by('-timestamp')

    def mask_identifier(identifier):
        if identifier and len(identifier) > 4:
            return identifier[:3] + '***' + identifier[-4:]
        return identifier

    context = {
        'transactions': transactions,
        'payments': payments,
        'mask_identifier': mask_identifier,
    }
    return render(request, 'core_bank/history.html', context)

@require_POST
def get_dni_info(request):
    dni = request.POST.get('dni')
    if not dni or not dni.isdigit() or len(dni) != 8:
        return JsonResponse({'error': 'DNI inválido. Debe ser de 8 dígitos numéricos.'}, status=400)

    if CustomUser.objects.filter(dni=dni).exists():
        return JsonResponse({'error': 'Este DNI ya está registrado.'}, status=409)

    url = "https://api.decolecta.com/v1/reniec/dni" 
    headers = {
        'Authorization': f'Bearer {DECOLECTA_API_TOKEN}', 
        'Content-Type': 'application/json' 
    }
    params = { 
        'numero': dni
    }
    
    if DECOLECTA_API_TOKEN is None:
        print("ERROR: DECOLECTA_API_TOKEN no está configurado en las variables de entorno.")
        return JsonResponse({'error': 'El token de la API no está configurado en el servidor.'}, status=500)
    elif not DECOLECTA_API_TOKEN.strip():
        print("ADVERTENCIA: DECOLECTA_API_TOKEN está vacío.")
        return JsonResponse({'error': 'El token de la API está vacío en el servidor.'}, status=500)

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() 

        data = response.json()
        if data.get('first_name'): 
            return JsonResponse({
                'success': True, 
                'nombres': data.get('first_name'), 
                'apellidoPaterno': data.get('first_last_name'), 
                'apellidoMaterno': data.get('second_last_name') 
            })
        else:
            error_message = data.get('message', 'No se encontró información para el DNI o la respuesta fue inválida.')
            return JsonResponse({'error': error_message}, status=404)
    except requests.exceptions.RequestException as e:
        if not os.getenv("DEBUG", "True").lower() == "true":
            print(f"Error al consultar API de DNI (Decolecta): {e}") 
        if hasattr(e, 'response') and e.response.status_code == 401:
            return JsonResponse({'error': 'Error de autenticación con la API de DNI. Verifica tu token.'}, status=401)
        return JsonResponse({'error': f'Error al conectar con el servicio de DNI: {e}'}, status=500)


@login_required
def get_user_balance_api(request):
    """
    API Endpoint para obtener el saldo del usuario autenticado.
    Esta función solo será llamada internamente por otras vistas (como el chatbot),
    no directamente por el frontend.
    """
    try:
        user_balance = request.user.balance
        # Convertir Decimal a string para evitar problemas de serialización JSON
        return JsonResponse({'balance': str(user_balance)})
    except Exception as e:
        if not os.getenv("DEBUG", "True").lower() == "true":
            print(f"Error al obtener saldo del usuario: {e}")
        return JsonResponse({'error': 'No se pudo obtener el saldo del usuario.'}, status=500)