from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import LibroForm, RegistroUsuarioForm
from .filters import LibroFilter
from .models import Libro


def home(request):
    total_libros = Libro.objects.count()
    libros_disponibles = Libro.objects.filter(disponible=True).count()
    return render(request, 'core/home.html', {
        'total_libros': total_libros,
        'libros_disponibles': libros_disponibles,
        'libros_prestados': total_libros - libros_disponibles,
    })


def lista_libros(request):
    filtro = LibroFilter(request.GET, queryset=Libro.objects.all())
    return render(request, 'core/lista_libros.html', {
        'filtro': filtro,
        'libros': filtro.qs,
    })


def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('registrar_libro')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, 'Tu cuenta está lista. Ya puedes registrar libros.')
            return redirect('registrar_libro')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'core/registro_usuario.html', {'form': form})


@login_required
def registrar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El libro se registró y ya está disponible en el catálogo.')
            return redirect('lista_libros')
    else:
        form = LibroForm()
    return render(request, 'core/registrar_libro.html', {'form': form})


@require_POST
def prestar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    if libro.disponible:
        libro.disponible = False
        libro.save(update_fields=['disponible'])
    return redirect('lista_libros')
