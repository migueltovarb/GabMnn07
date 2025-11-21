from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    ROLES = [
        ('administrador', 'Administrador'),
        ('recepcionista', 'Recepcionista'),
        ('visitante', 'Visitante'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='visitante')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    documento = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.rol})"

class Visitante(models.Model):
    TIPO_DOCUMENTO = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('PP', 'Pasaporte'),
        ('CE', 'Cédula de Extranjería'),
    ]
    
    nombre = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO)
    documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    motivo_visita = models.CharField(max_length=255)
    apartamento_visitado = models.CharField(max_length=50)
    persona_a_visitar = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombre} ({self.documento})"

class RegistroVisita(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, related_name='registros')
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='registros_creados')
    
    class Meta:
        verbose_name = 'Registro de Visita'
        verbose_name_plural = 'Registros de Visita'
        ordering = ['-fecha_entrada']
        indexes = [
            models.Index(fields=['-fecha_entrada']),
            models.Index(fields=['visitante', '-fecha_entrada']),
        ]
    
    def __str__(self):
        return f"{self.visitante.nombre} - {self.fecha_entrada.date()}"
    
    @property
    def en_edificio(self):
        return self.fecha_salida is None

class AuditoriaAccion(models.Model):
    ACCIONES = [
        ('CREATE', 'Crear'),
        ('UPDATE', 'Actualizar'),
        ('DELETE', 'Eliminar'),
        ('LOGIN', 'Iniciar Sesión'),
        ('LOGOUT', 'Cerrar Sesión'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='auditorias')
    accion = models.CharField(max_length=20, choices=ACCIONES)
    modelo = models.CharField(max_length=50)
    id_objeto = models.IntegerField()
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Auditoría de Acción'
        verbose_name_plural = 'Auditorías de Acciones'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['-fecha']),
            models.Index(fields=['usuario', '-fecha']),
        ]
    
    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha}"
