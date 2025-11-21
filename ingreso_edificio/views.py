# ===== FORMS.PY =====

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Visitante, RegistroVisita

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'telefono', 'documento']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_confirm']:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rol', 'telefono', 'is_active']

class RegistroVisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['nombre', 'tipo_documento', 'documento', 'email', 'telefono', 
                  'motivo_visita', 'apartamento_visitado', 'persona_a_visitar', 'descripcion']

class RegistroEntradaForm(forms.ModelForm):
    class Meta:
        model = RegistroVisita
        fields = ['visitante', 'observaciones']

class RegistroSalidaForm(forms.ModelForm):
    class Meta:
        model = RegistroVisita
        fields = ['visitante', 'observaciones']

class FiltroReporteForm(forms.Form):
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    visitante = forms.ModelChoiceField(queryset=Visitante.objects.all(), required=False)

# ===== VIEWS.PY =====

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
import csv

def es_administrador(user):
    return user.is_authenticated and user.rol == 'administrador'

def es_recepcionista(user):
    return user.is_authenticated and user.rol in ['administrador', 'recepcionista']

# ===== AUTENTICACIÓN =====
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                AuditoriaAccion.objects.create(
                    usuario=user,
                    accion='LOGIN',
                    modelo='Usuario',
                    id_objeto=user.id,
                    ip_address=get_client_ip(request)
                )
                messages.success(request, f"¡Bienvenido {user.get_full_name()}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect('login')

# ===== DASHBOARD =====
@login_required(login_url='login')
def dashboard(request):
    total_visitantes = Visitante.objects.count()
    ingresos_hoy = RegistroVisita.objects.filter(
        fecha_entrada__date=timezone.now().date()
    ).count()
    
    egresos_hoy = RegistroVisita.objects.filter(
        fecha_salida__date=timezone.now().date()
    ).count()
    
    usuarios_activos = Usuario.objects.filter(is_active=True).count()
    ultimas_visitas = RegistroVisita.objects.select_related('visitante')[:10]
    
    context = {
        'total_visitantes': total_visitantes,
        'ingresos_hoy': ingresos_hoy,
        'egresos_hoy': egresos_hoy,
        'usuarios_activos': usuarios_activos,
        'ultimas_visitas': ultimas_visitas,
    }
    
    return render(request, 'dashboard.html', context)

# ===== USUARIOS =====
@login_required(login_url='login')
@user_passes_test(es_administrador)
def crear_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            
            AuditoriaAccion.objects.create(
                usuario=request.user,
                accion='CREATE',
                modelo='Usuario',
                id_objeto=usuario.id,
                descripcion=f"Crear usuario {usuario.username}"
            )
            
            messages.success(request, "Usuario creado exitosamente")
            return redirect('listar_usuarios')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(es_administrador)
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

@login_required(login_url='login')
@user_passes_test(es_administrador)
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            
            AuditoriaAccion.objects.create(
                usuario=request.user,
                accion='UPDATE',
                modelo='Usuario',
                id_objeto=usuario.id,
                descripcion=f"Editar usuario {usuario.username}"
            )
            
            messages.success(request, "Usuario actualizado exitosamente")
            return redirect('listar_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario)
    
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required(login_url='login')
@user_passes_test(es_administrador)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        AuditoriaAccion.objects.create(
            usuario=request.user,
            accion='DELETE',
            modelo='Usuario',
            id_objeto=usuario.id,
            descripcion=f"Eliminar usuario {usuario.username}"
        )
        
        usuario.delete()
        messages.success(request, "Usuario eliminado exitosamente")
        return redirect('listar_usuarios')
    
    return render(request, 'usuarios/confirmar_eliminacion.html', {'usuario': usuario})

# ===== VISITANTES =====
@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def registrar_visitante(request):
    if request.method == 'POST':
        form = RegistroVisitanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Visitante registrado exitosamente")
            return redirect('listar_visitantes')
    else:
        form = RegistroVisitanteForm()
    
    return render(request, 'visitantes/registrar_visitante.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def listar_visitantes(request):
    visitantes = Visitante.objects.all()
    
    if request.GET.get('buscar'):
        q = request.GET.get('buscar')
        visitantes = visitantes.filter(
            Q(nombre__icontains=q) | Q(documento__icontains=q)
        )
    
    return render(request, 'visitantes/listar_visitantes.html', {'visitantes': visitantes})

@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def editar_visitante(request, visitante_id):
    visitante = get_object_or_404(Visitante, id=visitante_id)
    
    if request.method == 'POST':
        form = RegistroVisitanteForm(request.POST, instance=visitante)
        if form.is_valid():
            form.save()
            messages.success(request, "Visitante actualizado exitosamente")
            return redirect('listar_visitantes')
    else:
        form = RegistroVisitanteForm(instance=visitante)
    
    return render(request, 'visitantes/editar_visitante.html', {'form': form, 'visitante': visitante})

# ===== REGISTROS DE ENTRADA/SALIDA =====
@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def registrar_entrada(request):
    if request.method == 'POST':
        form = RegistroEntradaForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.registrado_por = request.user
            registro.save()
            messages.success(request, "Entrada registrada exitosamente")
            return redirect('dashboard')
    else:
        form = RegistroEntradaForm()
    
    visitantes_count = Visitante.objects.count()
    return render(request, 'registros/registrar_entrada.html', {
        'form': form,
        'visitantes_count': visitantes_count
    })

@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def registrar_salida(request):
    if request.method == 'POST':
        visitante_id = request.POST.get('visitante')
        visitante = get_object_or_404(Visitante, id=visitante_id)
        
        registro = RegistroVisita.objects.filter(
            visitante=visitante,
            fecha_salida__isnull=True
        ).last()
        
        if registro:
            registro.fecha_salida = timezone.now()
            registro.save()
            messages.success(request, "Salida registrada exitosamente")
        else:
            messages.error(request, "No hay registro de entrada para este visitante")
        
        return redirect('dashboard')
    
    visitantes = Visitante.objects.all()
    return render(request, 'registros/registrar_salida.html', {'visitantes': visitantes})

# ===== REPORTES Y CONSULTAS =====
@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def consultar_registros(request):
    registros = RegistroVisita.objects.select_related('visitante')
    
    if request.method == 'POST':
        form = FiltroReporteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['fecha_inicio']:
                registros = registros.filter(fecha_entrada__gte=form.cleaned_data['fecha_inicio'])
            if form.cleaned_data['fecha_fin']:
                registros = registros.filter(fecha_entrada__lte=form.cleaned_data['fecha_fin'])
            if form.cleaned_data['visitante']:
                registros = registros.filter(visitante=form.cleaned_data['visitante'])
    else:
        form = FiltroReporteForm()
    
    return render(request, 'registros/consultar_registros.html', {
        'registros': registros,
        'form': form
    })

@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def generar_reporte(request):
    registros = RegistroVisita.objects.select_related('visitante', 'registrado_por')
    
    if request.method == 'POST':
        form = FiltroReporteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['fecha_inicio']:
                registros = registros.filter(fecha_entrada__gte=form.cleaned_data['fecha_inicio'])
            if form.cleaned_data['fecha_fin']:
                registros = registros.filter(fecha_entrada__lte=form.cleaned_data['fecha_fin'])
        
        if request.POST.get('exportar_csv'):
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="reporte_ingresos.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Visitante', 'Documento', 'Entrada', 'Salida', 'Motivo'])
            
            for registro in registros:
                writer.writerow([
                    registro.visitante.nombre,
                    registro.visitante.documento,
                    registro.fecha_entrada,
                    registro.fecha_salida,
                    registro.visitante.motivo_visita
                ])
            
            return response
    else:
        form = FiltroReporteForm()
    
    return render(request, 'registros/generar_reporte.html', {
        'form': form,
        'registros': registros
    })

# ===== UTILIDADES =====
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from .models import AuditoriaAccion
