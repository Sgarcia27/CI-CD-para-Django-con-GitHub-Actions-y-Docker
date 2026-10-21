import django_filters
from django.db.models import Q

from .models import Libro


class LibroFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='buscar',
        label='Buscar por título o autor',
        widget=django_filters.widgets.forms.SearchInput(
            attrs={'placeholder': 'Ej. Gabriel García Márquez'}
        ),
    )
    disponible = django_filters.ChoiceFilter(
        choices=(('true', 'Disponibles'), ('false', 'Prestados')),
        method='filtrar_disponibilidad',
        label='Disponibilidad',
        empty_label='Todos',
    )

    class Meta:
        model = Libro
        fields = ()

    def buscar(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(titulo__icontains=value.strip()) | Q(autor__icontains=value.strip())
        )

    def filtrar_disponibilidad(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(disponible=True)
        if value == 'false':
            return queryset.filter(disponible=False)
        return queryset
