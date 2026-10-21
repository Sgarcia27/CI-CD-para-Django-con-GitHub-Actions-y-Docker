# Gestion

Proyecto Django configurado para conectarse a PostgreSQL.

Las dependencias se encuentran en `requirements.txt` e incluyen Django, PostgreSQL, Pillow para validar portadas, django-filter para filtrar el catálogo, WhiteNoise para estáticos y Gunicorn para despliegues Linux/Unix.

## Configurar PostgreSQL en Windows

1. Instala e inicia PostgreSQL si todavía no está instalado.
2. En pgAdmin, crea una base de datos llamada `gestion` (o usa otro nombre y actualiza `DB_NAME`).
3. Abre PowerShell en la carpeta del proyecto y define la conexión. Reemplaza el valor de `DB_PASSWORD` por la contraseña del usuario PostgreSQL:

   ```powershell
   $env:DB_NAME = "libro"
   $env:DB_USER = "postgres"
   $env:DB_PASSWORD = "TU_CONTRASENA"
   $env:DB_HOST = "localhost"
   $env:DB_PORT = "5432"
   ```

   Estas variables se aplican a esa ventana de PowerShell. Vuelve a definirlas en una nueva ventana.

4. Instala las dependencias y crea las tablas de Django:

   ```powershell
   python -m pip install -r requirements.txt
   python manage.py migrate
   ```

5. Inicia el sitio:

   ```powershell
   python manage.py runserver
   ```

La página está en <http://127.0.0.1:8000/> y el panel de administración en <http://127.0.0.1:8000/admin/>. Para crear un usuario administrador, ejecuta `python manage.py createsuperuser`.

Las portadas se cargan desde el formulario de registro y se guardan localmente en `media/portadas/`. En producción, configura almacenamiento persistente para archivos subidos por usuarios. El catálogo permite buscar por título/autor y filtrar por disponibilidad.

Para preparar archivos estáticos en un despliegue, ejecuta `python manage.py collectstatic`. En Linux/Unix, Gunicorn puede iniciar la aplicación con `gunicorn gestion.wsgi:application`.

No guardes la contraseña en el código. Si falta la configuración o PostgreSQL no está disponible, Django mostrará el error de conexión correspondiente.

Para despliegues, configura también `DJANGO_SECRET_KEY` con un valor aleatorio privado, `DJANGO_DEBUG=false` y `DJANGO_ALLOWED_HOSTS` con los dominios permitidos. La clave predeterminada solo sirve para desarrollo local.

## Cuentas de usuario

Los lectores pueden consultar el catálogo y marcar libros como prestados sin iniciar sesión. Para registrar libros en la colección, crea una cuenta desde `/cuenta/registro/` o inicia sesión en `/cuenta/ingresar/`. La autenticación usa el sistema integrado de Django y no añade dependencias a `requirements.txt`.
