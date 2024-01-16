from django.utils.translation import gettext_lazy as _


def manager_menu(request):
    links = []
    if request.user.groups.filter(name='Gate managers').exists():
        links = [
            {
                'title': _('Home page'),
                'link': 'manager',
                'icon': 'las la-home'
            },
            {
                'title': _('Tickets'),
                'link': 'manager-tickets',
                'icon': 'las la-ticket-alt'
            },
            {
                'title': _('Aircrafts'),
                'link': 'manager-aircrafts',
                'icon': 'las la-fighter-jet'
            },
            {
                'title': _('Aircraft models'),
                'link': 'manager-aircraft-models',
                'icon': 'las la-cog'
            },
            {
                'title': _('Airports'),
                'link': 'manager-airports',
                'icon': 'las la-map-marker'
            },
            {
                'title': _('Airport cities'),
                'link': 'manager-airport-cities',
                'icon': 'las la-map'
            },
            {
                'title': _('Company services'),
                'link': 'manager-services',
                'icon': 'las la-hamburger'
            },
            {
                'title': _('Company baggages'),
                'link': 'manager-service-baggages',
                'icon': 'las la-suitcase-rolling'
            },
            {
                'title': _('Flights'),
                'link': 'manager-flights',
                'icon': 'las la-plane-departure'
            },
            {
                'title': _('Flight services'),
                'link': 'manager-flight-services',
                'icon': 'las la-cart-plus'
            }
        ]

    return {'manager_menu': links}
