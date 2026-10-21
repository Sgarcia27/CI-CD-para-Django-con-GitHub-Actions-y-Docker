"""
URL configuration for gestion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core.views import home, lista_libros, prestar_libro, registrar_libro, registro_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('libros/', lista_libros, name='lista_libros'),
    path('libros/registrar/', registrar_libro, name='registrar_libro'),
    path('libros/<int:libro_id>/prestar/', prestar_libro, name='prestar_libro'),
    path('cuenta/registro/', registro_usuario, name='registro_usuario'),
    path(
        'cuenta/ingresar/',
        auth_views.LoginView.as_view(
            template_name='core/login.html',
            authentication_form=AuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path('cuenta/salir/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
