from django.db import models


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ['titulo', 'autor']
        verbose_name = 'libro'
        verbose_name_plural = 'libros'

    def __str__(self):
        return self.titulo
