# bank_project/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-dev") # Usa una clave de fallback solo para desarrollo
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(',')
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000 # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY' # Protección contra Clickjacking
    SECURE_BROWSER_XSS_FILTER = True # Protección contra XSS
    SECURE_CONTENT_TYPE_NOSNIFF = True # Previene ataques de olfateo de tipos MIME

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_extensions",
    'core_bank', # Nuestra aplicación principal de banca
    'chatbot', # Nuestra aplicación para el chatbot
    'crispy_forms', # Para formularios bonitos (opcional pero recomendado)
    'crispy_tailwind', # Si usas Tailwind CSS con Crispy Forms
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protección Clickjacking
]

ROOT_URLCONF = 'bank_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Directorio para plantillas globales
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bank_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de autenticación de contraseñas
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher', # Por defecto y seguro
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8, # Contraseña mínima de 8 caracteres
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# En bank_project/settings.py
# ...

# Configuración de autenticación personalizada
AUTH_USER_MODEL = 'core_bank.CustomUser'
LOGIN_REDIRECT_URL = 'core_bank:dashboard' # Redirige al dashboard después del login
LOGOUT_REDIRECT_URL = 'core_bank:login' # Redirige al login después del logout
LOGIN_URL = 'core_bank:login' # La URL para el login
# Configuración de i18n
LANGUAGE_CODE = 'es-pe' # Español de Perú
TIME_ZONE = 'America/Lima' # Zona horaria de Lima
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos (CSS, JS, imágenes)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Para producción

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Crispy Forms (si usas crispy_forms)
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Configuración de la sesión
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # La sesión expira al cerrar el navegador
SESSION_COOKIE_AGE = 1200 # 20 minutos de inactividad, puedes ajustar esto (en segundos)
SESSION_SAVE_EVERY_REQUEST = True # Guarda la sesión en cada solicitud (para actualizar el tiempo de expiración)
