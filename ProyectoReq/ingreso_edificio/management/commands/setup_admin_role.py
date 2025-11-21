from django.core.management.base import BaseCommand
from ingreso_edificio.models import Usuario

class Command(BaseCommand):
    help = 'Actualiza el rol de todos los superusers a administrador'

    def handle(self, *args, **options):
        usuarios = Usuario.objects.filter(is_superuser=True)
        
        if not usuarios.exists():
            self.stdout.write(self.style.WARNING('No hay superusers'))
            return
        
        for usuario in usuarios:
            if usuario.rol != 'administrador':
                usuario.rol = 'administrador'
                usuario.save()
                self.stdout.write(self.style.SUCCESS(f'✓ {usuario.username} ahora es administrador'))
            else:
                self.stdout.write(f'{usuario.username} ya es administrador')
