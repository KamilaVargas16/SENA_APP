from django.test import Client, TestCase
from django.urls import reverse
from aprendices.models import Aprendiz
from aprendices.forms import AprendizForm
from django.db import IntegrityError

class AprendizTestBase(TestCase):
    def setUp(self):
        self.aprendiz = Aprendiz.objects.create(
            document='123456789',
            firstname='Juan',
            lastname='Perez',
            phone='3200000000',
            email='juan.perez@example.com',
            birthdate='2000-01-01',
            city='Sogamoso',
            program='Desarrollo de Software',
        )
        
        self.client = Client()
        
class AprendizModelTest(AprendizTestBase):
    def test_aprendiz_se_crea_correctamente(self):
        aprendiz = Aprendiz.objects.get(document='123456789')
        self.assertEqual(aprendiz.document, '123456789')
        self.assertEqual(aprendiz.firstname, 'Juan')
        self.assertEqual(aprendiz.lastname, 'Perez')
        self.assertEqual(aprendiz.city, 'Sogamoso')
        
    def test_str_retorna_nombre_y_apellido(self):
        self.assertEqual(str(self.aprendiz), 'Juan Perez')
    
    def test_nombre_completo_concatena_correctamente(self):
        self.assertEqual(self.aprendiz.nombre_completo(), 'Juan Perez')
    
    def test_documento_identidad_debe_ser_unico(self):
        with self.assertRaises(IntegrityError):
            Aprendiz.objects.create(
                document='123456789',  # Mismo documento que el aprendiz existente
                firstname='otro',
                lastname='usuario',
                birthdate='2000-01-01',
                program='Sistemas',
            )
    
    def test_campos_opcionales_aceptan_null(self):
        aprendiz_minimo = Aprendiz.objects.create(
            document='987654321',
            firstname='Maria',
            lastname='Gomez',
            birthdate='2000-01-01',
            program='contabilidad',
        )
        self.assertIsNone(aprendiz_minimo.phone)
        self.assertIsNone(aprendiz_minimo.email)
        self.assertIsNone(aprendiz_minimo.city)
        
class AprendizFormTest(TestCase):
        def get_datos_validos(self):
            return{
                'document': '123456789',
                'firstname': 'Juan',
                'lastname': 'Perez',
                'phone': '3200000000',
                'email': 'juan.perez@example.com',
                'birthdate': '2000-01-01',
                'city': 'Sogamoso',
                'program': 'Desarrollo de Software',
            }
            
        def test_formulario_valido_con_datos_correctos(self):
            form = AprendizForm(data=self.get_datos_validos())
            self.assertTrue(form.is_valid(), msg=f'Errores: {form.errors}')

        def test_documento_con_letras_es_invalido(self):
            datos = self.get_datos_validos()
            datos['document'] = 'abc123'
            form = AprendizForm(data=datos)
            self.assertFalse(form.is_valid())
            self.assertIn('document', form.errors)
            self.assertIn('solo', str(form.errors['document']).lower())
            
        def test_telefono_con_letras_es_invalido(self):
            datos = self.get_datos_validos()
            datos['phone'] = 'abc123'
            form = AprendizForm(data=datos)
            self.assertFalse(form.is_valid())
            self.assertIn('phone', form.errors)
        
        def test_telefono_con_menos_de_10_digitos_es_invalido(self):
            datos = self.get_datos_validos()
            datos['phone'] = '12345'
            form = AprendizForm(data=datos)
            self.assertFalse(form.is_valid())
            self.assertIn('phone', form.errors)
            
        def test_correo_invalido_es_rechazado(self):
            datos = self.get_datos_validos()
            datos['email'] = 'esto_no_es_un_correo'
            form = AprendizForm(data=datos)
            self.assertFalse(form.is_valid())
            self.assertIn('email', form.errors)
            
        def test_campos_obligatorios_vacios_invalidan_formularios(self):
            form = AprendizForm(data={})
            self.assertFalse(form.is_valid())
            self.assertIn('document', form.errors)
            self.assertIn('firstname', form.errors)
            self.assertIn('lastname', form.errors)

class AprendizViewsTest(AprendizTestBase):

        def test_lista_aprendices_responde_200(self):
            url = reverse('aprendices:lista_aprendices')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_lista_aprendices_usa_template_correcto(self):
           url = reverse('aprendices:lista_aprendices')
           response = self.client.get(url)
           self.assertTemplateUsed(response, 'lista_aprendices.html')

        def test_lista_aprendices_contiene_el_aprendiz_creado(self):
            url = reverse('aprendices:lista_aprendices')
            response = self.client.get(url)
            self.assertContains(response, 'Juan')
            self.assertContains(response, 'Perez')
            
        def test_detalle_aprendiz_existente_responde_200(self):
            url = reverse('aprendices:detalle_aprendiz', args=[self.aprendiz.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '123456789') 
        
        def test_crear_aprendiz_con_datos_validos_redirige(self):
            url = reverse('aprendices:crear_aprendiz')
            datos = {
            'document': '5555555555',
            'firstname': 'Carlos',
            'lastname': 'Lopez',
            'phone': '3001112233',
            'email': 'carlos@test.com',
            'birthdate': '1999-11-05',
            'city': 'Cali',
            'program': 'Analisis y Desarrollo de Software',
            }
            response = self.client.post(url, data=datos)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(
                Aprendiz.objects.filter(document='5555555555').exists()
            )
            
        def test_crear_aprendiz_con_datos_invalidos_no_redirige(self):
            url = reverse('aprendices:crear_aprendiz')
            datos_invalidos = {
                'document': 'INVALIDO',
                'firstname': '',
                'lastname': 'Test',
                'birthdate': '2000-01-01',
                'program': 'Analisis',
            }
            response = self.client.post(url, data=datos_invalidos)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(
            Aprendiz.objects.filter(document='INVALIDO').exists()
            )

        def test_editar_aprendiz_actualiza_datos(self):
           url = reverse('aprendices:editar_aprendiz', args=[self.aprendiz.id])
           datos_actualizados = {
                  'document': '1234567890',
                  'firstname': 'Juan Carlos',
                  'lastname': 'Perez',
                  'phone': '3001234567',
                  'email': 'juan@test.com',
                  'birthdate': '2000-01-15',
                  'city': 'Barranquilla',
                  'program': 'Desarrollo de Software',
            }
           response = self.client.post(url, data=datos_actualizados)
           self.assertEqual(response.status_code, 302)
           self.aprendiz.refresh_from_db()
           self.assertEqual(self.aprendiz.firstname, 'Juan Carlos')
           self.assertEqual(self.aprendiz.city, 'Barranquilla')
           
       
        def test_eliminar_aprendiz_lo_borra_de_la_bd(self):
           aprendiz_id = self.aprendiz.id
           url = reverse('aprendices:eliminar_aprendiz', args=[aprendiz_id])
           response = self.client.post(url)
           self.assertEqual(response.status_code, 302)
           self.assertFalse(
                Aprendiz.objects.filter(id=aprendiz_id).exists()
        )
           
class AprendizURLTest(TestCase):
        
       def test_url_lista_aprendices_resuelve_correctamente(self):
          url = reverse('aprendices:lista_aprendices')
          self.assertEqual(url, '/aprendices/')

       def test_url_crear_aprendiz_resuelve_correctamente(self):
          url = reverse('aprendices:crear_aprendiz')
          self.assertEqual(url, '/aprendices/crear/')

       def test_url_detalle_aprendiz_resuelve_correctamente(self):
          url = reverse('aprendices:detalle_aprendiz', args=[1])
          self.assertEqual(url, '/aprendices/aprendiz/1/')

       def test_url_editar_aprendiz_resuelve_correctamente(self):
          url = reverse('aprendices:editar_aprendiz', args=[1])
          self.assertEqual(url, '/aprendices/1/editar/')

       def test_url_eliminar_aprendiz_resuelve_correctamente(self):
          url = reverse('aprendices:eliminar_aprendiz', args=[1])
          self.assertEqual(url, '/aprendices/1/eliminar/')