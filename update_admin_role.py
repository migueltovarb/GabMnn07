import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ingreso_edificio.models import Usuario

# Actualizar el rol del usuario admin
try:
    usuario = Usuario.objects.get(username='admin')
    usuario.rol = 'administrador'
    usuario.save()
    print(f"✓ Usuario '{usuario.username}' actualizado a rol: {usuario.rol}")
except Usuario.DoesNotExist:
    print("✗ Usuario 'admin' no encontrado")
except Exception as e:
    print(f"✗ Error: {str(e)}")
