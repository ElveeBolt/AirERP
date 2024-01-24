from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from apps.user.models import User

from .models import Airport, City
from .forms import CityManagerForm, AirportManagerForm


# Create your tests here.
class AirportManagerTestCase(TestCase):
    fixtures = ['airport.json']

    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='admin@example.com')
        self.user.set_password('admin')
        self.user.save()

        self.group = Group.objects.create(name='Supervisor')
        self.group.user_set.add(self.user)

        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_city_manager_list(self):
        response = self.client.get(reverse('manager-airport-cities'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('cities', response.context)

    def test_city_manager_view(self):
        response = self.client.get(reverse('manager-airport-city', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        city = response.context_data['city']
        self.assertEqual(city.name == 'Kyiv', True)

    def test_city_correct_form(self):
        response = self.client.get(reverse('manager-airport-city', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], CityManagerForm)

    def test_city_update(self):
        self.client.post(reverse('manager-airport-city', kwargs={'pk': 1}), {
            'name': 'Kyiv2',
            'country': 'Ukraine'
        })
        city = City.objects.get(pk=1)
        self.assertEqual(city.name, 'Kyiv2')

    def test_city_create(self):
        self.client.post(reverse('manager-airport-city-create'), {
            'name': 'Test city',
            'country': 'Test country'
        })
        city = City.objects.get(name='Test city')
        self.assertEqual(city.name, 'Test city')

    def test_airport_manager_list(self):
        response = self.client.get(reverse('manager-airports'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('airports', response.context)

    def test_airport_manager_view(self):
        response = self.client.get(reverse('manager-airport', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        city = response.context_data['airport']
        self.assertEqual(city.code == 'KBP', True)

    def test_airport_correct_form(self):
        response = self.client.get(reverse('manager-airport', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], AirportManagerForm)

    def test_airport_update(self):
        self.client.post(reverse('manager-airport', kwargs={'pk': 1}), {
            'code': 'KBP2',
            'name': 'Boryspil International Airport',
            'city': 1,
            'longitude': 50.33881090085334,
            'latitude': 30.8939703153421
        })
        airport = Airport.objects.get(pk=1)
        self.assertEqual(airport.code, 'KBP2')

    def test_airport_create(self):
        self.client.post(reverse('manager-airport-create'), {
            'code': 'KBP3',
            'name': 'Boryspil International Airport',
            'city': 1,
            'longitude': 50.33881090085334,
            'latitude': 30.8939703153421
        })
        airport = Airport.objects.get(code='KBP3')
        self.assertEqual(airport.code, 'KBP3')