from django.urls import path
from . import views

urlpatterns = [
    # ===== AUTENTICACIÓN =====
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ===== DASHBOARD =====
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ===== USUARIOS =====
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/listar/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # ===== VISITANTES =====
    path('visitantes/registrar/', views.registrar_visitante, name='registrar_visitante'),
    path('visitantes/listar/', views.listar_visitantes, name='listar_visitantes'),
    path('visitantes/<int:visitante_id>/editar/', views.editar_visitante, name='editar_visitante'),
    
    # ===== REGISTROS DE ENTRADA/SALIDA =====
    path('registros/entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('registros/salida/', views.registrar_salida, name='registrar_salida'),
    path('registros/consultar/', views.consultar_registros, name='consultar_registros'),
    path('registros/reporte/', views.generar_reporte, name='generar_reporte'),
]