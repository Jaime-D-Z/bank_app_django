from django.urls import path
from . import views

urlpatterns = [
    path('interact/', views.get_response, name='get_response'),
    # No es necesario una vista directa para chatbot_view si se incluye en otro template
]