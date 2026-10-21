from io import BytesIO
import tempfile

from PIL import Image
from django.test import TestCase
from django.test import override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Libro


def create_test_image():
    image = Image.new('RGB', (20, 20), color='green')
    image_file = BytesIO()
    image.save(image_file, format='JPEG')
    return SimpleUploadedFile('portada.jpg', image_file.getvalue(), content_type='image/jpeg')


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cada libro abre')
        self.assertContains(response, 'una nueva historia.')
        self.assertContains(response, 'Crear cuenta para registrar')
        self.assertContains(response, 'href="/cuenta/registro/"')


class LibroTests(TestCase):
    def setUp(self):
        self.media_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.media_directory.cleanup)
        self.media_settings = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.media_settings.enable()
        self.addCleanup(self.media_settings.disable)

    def test_new_book_is_available_by_default(self):
        libro = Libro.objects.create(titulo='Cien años de soledad', autor='Gabriel García Márquez')

        self.assertTrue(libro.disponible)

    def test_posting_to_borrow_book_marks_it_unavailable(self):
        libro = Libro.objects.create(titulo='Cien años de soledad', autor='Gabriel García Márquez')

        response = self.client.post('/libros/{}/prestar/'.format(libro.pk))

        self.assertRedirects(response, '/libros/')
        libro.refresh_from_db()
        self.assertFalse(libro.disponible)

    def test_book_list_displays_books(self):
        libro = Libro.objects.create(titulo='Cien años de soledad', autor='Gabriel García Márquez')

        response = self.client.get('/libros/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, libro.titulo)
        self.assertContains(response, libro.autor)

    def test_catalog_can_search_books_by_title_or_author(self):
        Libro.objects.create(titulo='El principito', autor='Antoine de Saint-Exupéry')
        Libro.objects.create(titulo='La tregua', autor='Mario Benedetti')

        response = self.client.get('/libros/', {'q': 'principito'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['libros'].values_list('titulo', flat=True)), ['El principito'])

        response = self.client.get('/libros/', {'q': 'Benedetti'})
        self.assertEqual(list(response.context['libros'].values_list('titulo', flat=True)), ['La tregua'])

    def test_catalog_can_filter_available_books(self):
        Libro.objects.create(titulo='Disponible', autor='Autora')
        Libro.objects.create(titulo='Prestado', autor='Autor', disponible=False)

        response = self.client.get('/libros/', {'disponible': 'true'})

        self.assertEqual(list(response.context['libros'].values_list('titulo', flat=True)), ['Disponible'])

    def test_register_page_loads_form(self):
        self.client.force_login(get_user_model().objects.create_user(username='reader', password='StrongPass123!'))
        response = self.client.get('/libros/registrar/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Título del libro')
        self.assertContains(response, 'Autor o autora')

    def test_registering_book_saves_it_as_available(self):
        self.client.force_login(get_user_model().objects.create_user(username='reader', password='StrongPass123!'))
        response = self.client.post('/libros/registrar/', {
            'titulo': 'El principito',
            'autor': 'Antoine de Saint-Exupéry',
            'portada': create_test_image(),
        })

        self.assertRedirects(response, '/libros/')
        libro = Libro.objects.get(titulo='El principito')
        self.assertEqual(libro.autor, 'Antoine de Saint-Exupéry')
        self.assertTrue(libro.disponible)
        self.assertTrue(libro.portada)

    def test_registering_book_requires_title_and_author(self):
        self.client.force_login(get_user_model().objects.create_user(username='reader', password='StrongPass123!'))
        response = self.client.post('/libros/registrar/', {'titulo': '', 'autor': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Libro.objects.count(), 0)
        self.assertContains(response, 'Este campo es obligatorio.')

    def test_book_registration_requires_login(self):
        response = self.client.get('/libros/registrar/')

        self.assertRedirects(response, '/cuenta/ingresar/?next=/libros/registrar/')

    def test_user_can_create_account_and_is_logged_in(self):
        response = self.client.post('/cuenta/registro/', {
            'username': 'newreader',
            'password1': 'StrongPass123!@#',
            'password2': 'StrongPass123!@#',
        })

        self.assertRedirects(response, '/libros/registrar/')
        self.assertTrue(get_user_model().objects.filter(username='newreader').exists())
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_can_log_in_and_log_out(self):
        user = get_user_model().objects.create_user(username='reader', password='StrongPass123!')

        response = self.client.post('/cuenta/ingresar/', {
            'username': user.username,
            'password': 'StrongPass123!',
        })
        self.assertRedirects(response, '/')
        self.assertTrue('_auth_user_id' in self.client.session)

        response = self.client.post('/cuenta/salir/')
        self.assertRedirects(response, '/')
        self.assertFalse('_auth_user_id' in self.client.session)
