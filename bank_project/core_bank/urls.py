from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login_view, name='login'), # Ruta para login
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('services/', views.services_view, name='services'),
    path('history/', views.history_view, name='history'),
    path('get_dni_info/', views.get_dni_info, name='get_dni_info'),
    
    # NUEVA RUTA: Endpoint API para el saldo del usuario
    path('api/balance/', views.get_user_balance_api, name='get_user_balance_api'),
]
