from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.aircraft.models import AircraftModel
from apps.flight.filters import FlightFilter
from apps.user.mixins import StaffMixin


# Create your views here.
class IndexView(TemplateView):
    template_name = 'user/apps/page/index.html'
    extra_context = {
        'title': _('AirERP'),
        'subtitle': _('Compare prices. Book the best tickets. Enjoy your journey.')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FlightFilter()
        context['aircrafts'] = AircraftModel.objects.all()[:3]
        return context


class IndexManagerView(StaffMixin, TemplateView):
    template_name = 'manager/apps/page/index.html'
    extra_context = {
        'title': _('AirERP'),
        'subtitle': _('Compare prices. Book the best tickets. Enjoy your journey.')
    }