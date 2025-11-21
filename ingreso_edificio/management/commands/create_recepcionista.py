from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un usuario recepcionista de prueba'

    def handle(self, *args, **options):
        username = 'recepcionista'
        email = 'recepcionista@edificio.com'
        password = 'Recepcionista123!'
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'✗ El usuario {username} ya existe'))
            return
        
        # Crear el usuario recepcionista
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Recepcionista',
            last_name='Sistema',
            rol='recepcionista',
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Usuario recepcionista creado exitosamente'))
        self.stdout.write(f'  Usuario: {username}')
        self.stdout.write(f'  Contraseña: {password}')
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Rol: recepcionista')
