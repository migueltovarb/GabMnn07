# Sistema Integral de Gestión de Ingreso a Edificios

**Universidad Cooperativa de Colombia**  
**Ingeniería de Software**  
**Autor:** Gabriel Alejandro Chicaiza Mora

---

## 📋 Descripción

Sistema web desarrollado con Django para la gestión y control de acceso de visitantes a edificios. Incluye registro de entradas/salidas, gestión de usuarios, generación de reportes y auditoría de acciones.

## ✨ Características Principales

- ✅ Autenticación de usuarios con roles (Administrador, Recepcionista)
- ✅ Registro y gestión de visitantes
- ✅ Control de entradas y salidas con timestamps
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Generación y exportación de reportes (CSV)
- ✅ Sistema de auditoría completo
- ✅ Interfaz web responsiva y moderna
- ✅ Validaciones de datos robustas

## 🛠️ Requisitos del Sistema

### Requisitos Mínimos (según SRS)
- **Sistema Operativo:** Windows 10 o superior
- **Memoria RAM:** 4 GB
- **Procesador:** Intel Core i5 (2ª generación o superior)
- **Espacio en disco:** 1 GB disponible
- **Navegador:** Google Chrome o Mozilla Firefox

### Requisitos de Software
- Python 3.10 o superior
- Django 5.0+
- Base de datos SQL (SQLite por defecto, MySQL/PostgreSQL opcional)

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/migueltovarb/GabMnn07.git
cd GabMnn07
```

### 2. Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install django
```

Para producción (con MySQL/PostgreSQL):
```bash
pip install django mysqlclient  # Para MySQL
# O
pip install django psycopg2-binary  # Para PostgreSQL
```

### 4. Estructura del Proyecto

Crear la siguiente estructura de carpetas:

```
GabMnn07/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── ingreso_edificio/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── usuarios/
│   ├── visitantes/
│   ├── registros/
│   └── reportes/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── manage.py
└── requirements.txt
```

### 5. Configurar Base de Datos

El proyecto usa SQLite por defecto. Para cambiar a MySQL o PostgreSQL, editar `settings.py`:

**MySQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ingreso_edificio_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Realizar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingresar:
- Username
- Email
- Password (mínimo 8 caracteres)

### 8. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

Acceder a: `http://127.0.0.1:8000/`

---

## 👥 Usuarios y Roles

### Administrador
- Gestión completa de usuarios
- Acceso a todos los módulos
- Generación de reportes
- Eliminación de registros

### Recepcionista
- Registro de visitantes
- Control de entradas/salidas
- Consulta de registros
- Generación de reportes básicos

---

## 📖 Guía de Uso

### 1. Inicio de Sesión
1. Acceder a la URL del sistema
2. Ingresar usuario y contraseña
3. El sistema redirige al dashboard según el rol

### 2. Registrar Visitante Nuevo
1. Ir a **Visitantes → Crear Visitante**
2. Completar formulario:
   - Nombre completo (obligatorio)
   - Documento (solo números, obligatorio)
   - Teléfono (opcional)
   - Email (opcional)
   - Empresa (opcional)
3. Clic en **Guardar**

### 3. Registrar Entrada
1. Ir a **Registrar Entrada**
2. Seleccionar visitante de la lista
3. Completar:
   - Motivo de visita
   - Persona o dependencia a visitar
   - Observaciones (opcional)
4. Clic en **Registrar Entrada**
   - La hora se registra automáticamente
   - El sistema valida que no tenga entrada activa

### 4. Registrar Salida
1. Desde el Dashboard o Lista de Registros
2. Buscar visitante activo
3. Clic en **Registrar Salida**
4. Confirmar acción
   - Se calcula automáticamente el tiempo de permanencia

### 5. Generar Reportes
1. Ir a **Reportes**
2. Aplicar filtros:
   - Rango de fechas
   - Visitante específico
   - Estado (activo/finalizado)
3. Ver resultados en pantalla
4. Exportar a CSV si es necesario

### 6. Gestión de Usuarios (Solo Administrador)
1. Ir a **Usuarios**
2. Opciones disponibles:
   - **Crear:** Nuevo usuario con rol asignado
   - **Editar:** Modificar datos de usuario
   - **Eliminar:** Borrar usuario del sistema

---

## 🔒 Seguridad

### Características Implementadas
- ✅ Contraseñas cifradas (hash)
- ✅ Validación de campos en cliente y servidor
- ✅ Protección CSRF
- ✅ Control de acceso por roles
- ✅ Sesiones con tiempo de expiración
- ✅ Auditoría de acciones
- ✅ Registro de IP en acciones críticas

### Para Producción
Descomentar en `settings.py`:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

---

## 📊 Historias de Usuario Implementadas

| ID | Historia de Usuario | Estado |
|----|---------------------|--------|
| HU001 | Registro de usuarios | ✅ |
| HU002 | Inicio y cierre de sesión | ✅ |
| HU003 | Gestión de usuarios | ✅ |
| HU004 | Registro de visitantes | ✅ |
| HU005 | Control de ingreso y salida | ✅ |
| HU006 | Creación de registros de visita | ✅ |
| HU007 | Consulta de registros | ✅ |
| HU008 | Generación de reportes | ✅ |
| HU009 | Almacenamiento de datos | ✅ |
| HU010 | Eliminación de registros | ✅ |
| HU011 | Validación de datos | ✅ |
| HU012 | Interfaz web | ✅ |

---

## 🎨 Diseño Visual

El sistema sigue el **Style Tile** especificado:

- **Tipografía:** Sans Serif (Arial, Roboto)
- **Colores:**
  - Negro: `#000000`
  - Gris oscuro: `#3b3b3b`
  - Gris claro: `#e3e3e3`
- **Estilo:** Formal, minimalista, corporativo
- **Elementos:** Botones rectangulares, formularios limpios, espaciado amplio

---

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install django
```

### Error de migraciones
```bash
python manage.py makemigrations --empty ingreso_edificio
python manage.py migrate
```

### Puerto 8000 en uso
```bash
python manage.py runserver 8080
```

### Olvidé la contraseña del superusuario
```bash
python manage.py changepassword nombre_usuario
```

---

## 📝 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar pruebas
python manage.py test

# Acceder a la shell de Django
python manage.py shell

# Ver estructura de tablas
python manage.py dbshell
```

---

## 📚 Referencias

- Young, R. R. (2004). *Requirements Engineering and Management for Software Development Projects*. Artech House.
- Django Software Foundation. (2025). Django Documentation.
- ISO/IEC 25010 - Calidad de Software

---

## 👨‍💻 Autor

**Gabriel Alejandro Chicaiza Mora**  
Universidad Cooperativa de Colombia  
Ingeniería de Software  
2025

---

## 📄 Licencia

Este proyecto es académico y está desarrollado con fines educativos.

---

## 🔄 Próximas Versiones

- [ ] Integración con reconocimiento facial
- [ ] Panel predictivo con IA
- [ ] Integración con videovigilancia
- [ ] Identificación biométrica
- [ ] App móvil para guardias de seguridad
- [ ] Notificaciones en tiempo real
- [ ] Dashboard con gráficos interactivos

---

## 📞 Soporte

Para reportar problemas o sugerencias:
1. Crear un **Issue** en el repositorio
2. Contactar al autor vía email institucional
3. Revisar la documentación del wiki

---

**¡Gracias por usar el Sistema de Gestión de Ingreso a Edificios!** 🏢