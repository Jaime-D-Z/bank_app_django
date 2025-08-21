from django.shortcuts import render
from django.http import JsonResponse
import cohere
import os
from dotenv import load_dotenv
from core_bank import views as core_bank_views # Importar vistas de core_bank
from django.contrib.auth.models import AnonymousUser # Para verificar si el usuario está autenticado

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')

def get_response(request):
    user_message = request.GET.get('message', '').lower() # Convertir a minúsculas para coincidencia de palabras clave

    # Palabras clave para detectar si el usuario pregunta por su saldo
    balance_keywords = ["cuanto dinero tengo", "cuál es mi saldo", "mi dinero", "saldo de mi cuenta", "consultar saldo", "ver mi saldo"]
    
    # Verificar si alguna palabra clave de saldo está en el mensaje del usuario
    is_asking_for_balance = any(keyword in user_message for keyword in balance_keywords)

    if is_asking_for_balance:
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Llamar directamente a la función de vista de core_bank para obtener el saldo
            # Pasamos el objeto request actual para que la vista tenga el usuario
            balance_response_json = core_bank_views.get_user_balance_api(request)
            balance_data = balance_response_json.json() # Parsear el contenido de JsonResponse

            if 'balance' in balance_data:
                balance = balance_data['balance']
                return JsonResponse({'response': f"Tu saldo actual es de S/ {balance}. ¿Hay algo más en lo que pueda ayudarte?"})
            else:
                # Si la API interna no pudo obtener el saldo
                return JsonResponse({'response': 'Lo siento, no pude obtener tu saldo en este momento. Por favor, inténtalo de nuevo.'}, status=500)
        else:
            # Si el usuario no está autenticado y pregunta por el saldo
            return JsonResponse({'response': 'Para consultar tu saldo, necesitas iniciar sesión. Por favor, inicia sesión para acceder a tu información personal.'})

    # Si no se pregunta por el saldo, proceder con Cohere como de costumbre
    contexto = """
Eres un asesor bancario profesional.
Responde de manera amable y clara.
Tus respuestas deben ser breves: máximo 2-3 frases.
Solo da información sobre cuentas, préstamos, tarjetas y transferencias.
No inventes información sobre clientes.
Evita explicaciones largas o redundantes.
"""

    try:
        respuesta = co.chat(
            model="command-r-plus", # O el modelo de Cohere que prefieras
            message=user_message,
            preamble=contexto,
            max_tokens=60
        )
        return JsonResponse({'response': respuesta.text})
    except cohere.CohereError as e:
        if not os.getenv("DEBUG", "True").lower() == "true":
            print(f"Error de Cohere API: {e}")
        return JsonResponse({'response': 'Lo siento, no puedo procesar tu solicitud en este momento. Por favor, inténtalo más tarde.'}, status=500)
    except Exception as e:
        if not os.getenv("DEBUG", "True").lower() == "true":
            print(f"Error inesperado en el chatbot: {e}")
        return JsonResponse({'response': 'Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo.'}, status=500)
