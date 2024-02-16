from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin


class StaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class GateManagerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Gate managers').exists()


class CheckinManagerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Checkin managers').exists()


class SupervisorManagerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Supervisor').exists()
