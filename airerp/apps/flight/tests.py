from urllib.parse import urlencode

from django.test import TestCase, Client
from django.urls import reverse

from apps.user.models import User


# Create your tests here.
class FlightTestCase(TestCase):
    fixtures = ['aircraft.json', 'airport.json', 'flight.json', 'service.json']

    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com')
        self.user.set_password('user')
        self.user.save()

        self.client = Client()
        self.client.login(username='user', password='user')

    def test_flight_list(self):
        response = self.client.get(reverse('flights'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('flights', response.context)

    def test_aircraft_filter_list(self):
        params = {'departure_from': 1, 'arrival_to': 3, 'departure_time': '2024-01-20', 'seat_class': 'E'}
        response = self.client.get(reverse('flights') + '?' + urlencode(params))
        self.assertEqual(response.status_code, 200)
        flights = response.context_data['flights']
        self.assertEqual(flights.count() == 2, True)

    def test_aircraft_filter_single_list(self):
        params = {'title': 'Airbus A330', 'manufacturer': 1}
        response = self.client.get(reverse('aircrafts') + '?' + urlencode(params))
        self.assertEqual(response.status_code, 200)
        aircrafts = response.context_data['aircrafts']
        self.assertEqual(aircrafts.count() == 1, True)
