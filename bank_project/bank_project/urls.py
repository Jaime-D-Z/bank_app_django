from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # App principal del banco
    path('bank/', include(('core_bank.urls', 'core_bank'), namespace='core_bank')),

    # Chatbot (opcional)
    path('chatbot/', include(('chatbot.urls', 'chatbot'), namespace='chatbot')),

    # Redirige la raíz al login
    path('', lambda request: redirect('core_bank:login'), name='root'),
]
