
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

class CustomUser(AbstractUser):
    # DNI como CharField para manejar ceros iniciales y validaciones de longitud.
    # unique=True asegura que no haya DNIs duplicados.
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Campos de nombres y apellidos (opcionales, ya que AbstractUser ya tiene first_name y last_name)
    # Sin embargo, los incluimos para ser explícitos con el autocompletado del API
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Nombres")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Apellidos")

    def save(self, *args, **kwargs):
        # Asigna un saldo inicial de 10,000.00 a nuevos usuarios
        if not self.pk: # Solo si es un nuevo usuario (no tiene PK aún)
            self.balance = Decimal('10000.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.dni})"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('transferencia', 'Transferencia'),
        ('pago_servicio', 'Pago de Servicio'),
    )

    sender = models.ForeignKey(CustomUser, related_name='sent_transactions', on_delete=models.CASCADE, verbose_name="Remitente")
    receiver = models.ForeignKey(CustomUser, related_name='received_transactions', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Destinatario")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="Tipo de Transacción")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        if self.receiver:
            return f"De {self.sender.username} a {self.receiver.username} - {self.amount} ({self.transaction_type})"
        return f"De {self.sender.username} - {self.amount} ({self.transaction_type})"

    class Meta:
        ordering = ['-timestamp'] # Ordena las transacciones por fecha descendente

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Servicio")
    # No es necesario un campo 'price' aquí si el monto es variable por pago
    # Si cada servicio tuviera un precio fijo, lo añadiríamos aquí.

    def __str__(self):
        return self.name

class ServicePayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Usuario")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Servicio")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora del Pago")
    invoice_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Factura/Recibo")

    def __str__(self):
        return f"Pago de {self.amount} a {self.service.name} por {self.user.username}"

    class Meta:
        ordering = ['-timestamp']