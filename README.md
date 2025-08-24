# 🏦 Bank App Django

Una aplicación bancaria completa desarrollada con Django que proporciona funcionalidades esenciales de banca digital, incluyendo gestión de cuentas, transferencias, historial de transacciones y más.

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

## 📋 Tabla de Contenidos

- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Funcionalidades](#funcionalidades)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## ✨ Características

- **Autenticación de Usuarios**: Registro, inicio de sesión y gestión de perfiles
- **Gestión de Cuentas**: Creación y administración de cuentas bancarias
- **Transferencias**: Transferencias entre cuentas propias y a terceros
- **Depósitos y Retiros**: Operaciones básicas de depósito y retiro
- **Historial de Transacciones**: Visualización completa del historial financiero
- **Dashboard Interactivo**: Panel de control con resumen de cuentas
- **Seguridad**: Implementación de medidas de seguridad bancaria
- **Responsive Design**: Interfaz adaptable a dispositivos móviles y desktop

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.x, Python 3.8+
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Autenticación**: Django Authentication System
- **Estilos**: Bootstrap 5, CSS personalizado

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/Jaime-D-Z/bank_app_django.git
   cd bank_app_django
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crea un superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecuta el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

7. **Accede a la aplicación**
   
   Abre tu navegador y ve a `http://localhost:8000`

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# Para producción con PostgreSQL
# DATABASE_URL=postgres://usuario:contraseña@host:puerto/nombre_bd
```

### Configuración de Base de Datos

Para usar PostgreSQL en producción, actualiza el archivo `settings.py`:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

## 💡 Uso

### Para Usuarios

1. **Registro**: Crea una nueva cuenta de usuario
2. **Inicio de Sesión**: Accede con tus credenciales
3. **Crear Cuenta Bancaria**: Establece tu primera cuenta bancaria
4. **Realizar Transacciones**: Deposita, retira o transfiere dinero
5. **Ver Historial**: Consulta todas tus transacciones

### Para Administradores

1. Accede al panel de administración en `/admin`
2. Gestiona usuarios, cuentas y transacciones
3. Supervisa la actividad del sistema

## 🔧 Funcionalidades

### Gestión de Usuarios
- Registro de nuevos usuarios
- Autenticación segura
- Perfiles de usuario personalizables
- Recuperación de contraseñas

### Sistema Bancario
- Creación de múltiples cuentas por usuario
- Diferentes tipos de cuenta (Ahorro, Corriente)
- Validación de saldos y límites
- Generación de números de cuenta únicos

### Transacciones
- Depósitos instantáneos
- Retiros con validación de saldo
- Transferencias entre cuentas
- Registro detallado de transacciones
- Estados de transacción (Pendiente, Completada, Fallida)

### Seguridad
- Encriptación de datos sensibles
- Validación de transacciones
- Logs de actividad
- Protección CSRF

## 📁 Estructura del Proyecto

```
bank_app_django/
├── bank_app/                 # Aplicación principal
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Vistas y lógica
│   ├── urls.py              # URLs de la app
│   └── forms.py             # Formularios
├── bank_project/            # Configuración del proyecto
│   ├── settings.py          # Configuraciones
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
├── static/                  # Archivos estáticos
├── media/                   # Archivos multimedia
├── templates/               # Templates base
├── requirements.txt         # Dependencias
├── manage.py               # Script de gestión
└── README.md               # Este archivo
```

## 🌐 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página principal |
| POST | `/register/` | Registro de usuario |
| POST | `/login/` | Inicio de sesión |
| GET | `/dashboard/` | Panel de control |
| POST | `/create-account/` | Crear cuenta bancaria |
| POST | `/transfer/` | Realizar transferencia |
| GET | `/transactions/` | Historial de transacciones |
| POST | `/deposit/` | Realizar depósito |
| POST | `/withdraw/` | Realizar retiro |

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres contribuir a este proyecto:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Reportar Bugs

Si encuentras un bug, por favor abre un issue describiendo:
- El problema encontrado
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Screenshots si es relevante

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

