from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from apps.user.models import User

from .models import Service, Baggage
from .forms import ServiceManagerForm, BaggageManagerForm


# Create your tests here.
class ServiceManagerTestCase(TestCase):
    fixtures = ['service.json']

    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='admin@example.com')
        self.user.set_password('admin')
        self.user.save()

        self.group = Group.objects.create(name='Supervisor')
        self.group.user_set.add(self.user)

        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_service_manager_list(self):
        response = self.client.get(reverse('manager-services'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('services', response.context)

    def test_service_manager_view(self):
        response = self.client.get(reverse('manager-service', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        service = response.context_data['service']
        self.assertEqual(service.name == 'Wi-Fi access', True)

    def test_service_correct_form(self):
        response = self.client.get(reverse('manager-service', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], ServiceManagerForm)

    def test_service_update(self):
        self.client.post(reverse('manager-service', kwargs={'pk': 1}), {
            'name': 'Wi-Fi access 2',
            'description': 'Description',
            'icon': 'la las-wifi',
            'max_quantity': 10
        })
        service = Service.objects.get(pk=1)
        self.assertEqual(service.name, 'Wi-Fi access 2')

    def test_service_create(self):
        self.client.post(reverse('manager-service-create'), {
            'name': 'Wi-Fi access 3',
            'description': 'Description',
            'icon': 'la las-wifi',
            'max_quantity': 10
        })
        service = Service.objects.get(name='Wi-Fi access 3')
        self.assertEqual(service.name, 'Wi-Fi access 3')

    def test_baggage_manager_list(self):
        response = self.client.get(reverse('manager-service-baggages'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('baggages', response.context)

    def test_baggage_manager_view(self):
        response = self.client.get(reverse('manager-service-baggage', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        baggage = response.context_data['baggage']
        self.assertEqual(baggage.name == 'First additional bag up to 10 kg', True)

    def test_baggage_correct_form(self):
        response = self.client.get(reverse('manager-service-baggage', kwargs={'pk': 1}))
        self.assertIsInstance(response.context['form'], BaggageManagerForm)

    def test_baggage_update(self):
        self.client.post(reverse('manager-service-baggage', kwargs={'pk': 1}), {
            'name': 'First additional bag up to 50 kg',
            'description': ''
        })
        baggage = Baggage.objects.get(pk=1)
        self.assertEqual(baggage.name, 'First additional bag up to 50 kg')

    def test_baggage_create(self):
        self.client.post(reverse('manager-service-baggage-create'), {
            'name': 'First additional bag up to 60 kg',
            'description': ''
        })
        baggage = Baggage.objects.get(name='First additional bag up to 60 kg')
        self.assertEqual(baggage.name, 'First additional bag up to 60 kg')