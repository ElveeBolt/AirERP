from unittest.mock import patch

from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from apps.user.models import User

from .models import Aircraft, AircraftModel, AircraftManufacturerModel
from .forms import AircraftManagerForm, AircraftModelManagerForm, AircraftManufacturerManagerForm


# Create your tests here.
class ServiceManagerTestCase(TestCase):
    fixtures = ['aircraft.json']

    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='admin@example.com')
        self.user.set_password('admin')
        self.user.save()

        self.group = Group.objects.create(name='Supervisor')
        self.group.user_set.add(self.user)

        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_manufacturer_manager_list(self):
        response = self.client.get(reverse('manager-aircraft-manufacturers'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('manufacturers', response.context)

    def test_manufacturer_manager_view(self):
        response = self.client.get(reverse('manager-aircraft-manufacture', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        manufacturer = response.context_data['manufacture']
        self.assertEqual(manufacturer.title == 'Airbus', True)

    def test_manufacturer_correct_form(self):
        response = self.client.get(reverse('manager-aircraft-manufacture', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], AircraftManufacturerManagerForm)

    def test_manufacturer_update(self):
        self.client.post(reverse('manager-aircraft-manufacture', kwargs={'pk': 1}), {
            'title': 'Airbus 2',
            'description': 'Description',
        })
        manufacturer = AircraftManufacturerModel.objects.get(pk=1)
        self.assertEqual(manufacturer.title, 'Airbus 2')

    def test_manufacturer_create(self):
        self.client.post(reverse('manager-aircraft-manufacture-create'), {
            'title': 'Airbus 3',
            'description': 'Description',
        })
        manufacturer = AircraftManufacturerModel.objects.get(title='Airbus 3')
        self.assertEqual(manufacturer.title, 'Airbus 3')

    def test_model_manager_list(self):
        response = self.client.get(reverse('manager-aircraft-models'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('aircrafts', response.context)

    def test_model_manager_view(self):
        response = self.client.get(reverse('manager-aircraft-model', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        aircraft = response.context_data['aircraft']
        self.assertEqual(aircraft.title == 'Airbus A330', True)

    def test_model_correct_form(self):
        response = self.client.get(reverse('manager-aircraft-model', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], AircraftModelManagerForm)

    # def test_model_update(self, mock_upload):
    #     mock_upload.return_value = 'path/to/mock/image.jpg'
    #     self.client.post(reverse('manager-aircraft-model', kwargs={'pk': 1}), {
    #         'title': 'Airbus A330 2',
    #         'description': 'Description',
    #         'manufacturer': 1,
    #         'manufacturer_year': 1990,
    #     })
    #     aircraft = AircraftModel.objects.get(pk=1)
    #     self.assertEqual(aircraft.title, 'Airbus A330 2')
    #
    # def test_baggage_create(self):
    #     self.client.post(reverse('manager-service-baggage-create'), {
    #         'name': 'First additional bag up to 60 kg',
    #         'description': ''
    #     })
    #     baggage = Baggage.objects.get(name='First additional bag up to 60 kg')
    #     self.assertEqual(baggage.name, 'First additional bag up to 60 kg')