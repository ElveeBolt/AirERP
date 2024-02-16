from urllib.parse import urlencode

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from apps.user.models import User

from .models import Aircraft, AircraftManufacturerModel
from .forms import AircraftManagerForm, AircraftModelManagerForm, AircraftManufacturerManagerForm


# Create your tests here.
class AircraftManagerTestCase(TestCase):
    fixtures = ['aircraft.json', 'airport.json']

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

    def test_aircraft_manager_list(self):
        response = self.client.get(reverse('manager-aircrafts'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('aircrafts', response.context)

    def test_aircraft_manager_view(self):
        response = self.client.get(reverse('manager-aircraft', kwargs={'pk': 5}))
        self.assertEqual(response.status_code, 200)
        aircraft = response.context_data['aircraft']
        self.assertEqual(aircraft.title == 'A330', True)

    def test_aircraft_correct_form(self):
        response = self.client.get(reverse('manager-aircraft', kwargs={'pk': 5}))
        self.assertIsInstance(response.context['form'], AircraftManagerForm)

    def test_aircraft_update(self):
        self.client.post(reverse('manager-aircraft', kwargs={'pk': 5}), {
            'title': 'A330 2',
            'model': 1,
            'current_airport': 1,
            'total_seats': 10,
            'window_seats': 2,
            'extra_legroom_seats': 2,
            'aisle_seats': 2
        })
        aircraft = Aircraft.objects.get(pk=5)
        self.assertEqual(aircraft.title, 'A330 2')

    def test_aircraft_create(self):
        self.client.post(reverse('manager-aircraft-create'), {
            'title': 'A330 3',
            'model': 1,
            'current_airport': 1,
            'total_seats': 10,
            'window_seats': 2,
            'extra_legroom_seats': 2,
            'aisle_seats': 2
        })
        aircraft = Aircraft.objects.get(title='A330 3')
        self.assertEqual(aircraft.title, 'A330 3')


class AircraftTestCase(TestCase):
    fixtures = ['aircraft.json', 'airport.json']

    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com')
        self.user.set_password('user')
        self.user.save()

        self.client = Client()
        self.client.login(username='user', password='user')

    def test_aircraft_list(self):
        response = self.client.get(reverse('aircrafts'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('aircrafts', response.context)

    def test_aircraft_filter_list(self):
        params = {'manufacturer': 1}
        response = self.client.get(reverse('aircrafts') + '?' + urlencode(params))
        self.assertEqual(response.status_code, 200)
        aircrafts = response.context_data['aircrafts']
        self.assertEqual(aircrafts.count() == 3, True)

    def test_aircraft_filter_single_list(self):
        params = {'title': 'Airbus A330', 'manufacturer': 1}
        response = self.client.get(reverse('aircrafts') + '?' + urlencode(params))
        self.assertEqual(response.status_code, 200)
        aircrafts = response.context_data['aircrafts']
        self.assertEqual(aircrafts.count() == 1, True)
