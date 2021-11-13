from django.contrib.auth.mixins import UserPassesTestMixin


class IsSuperUserOrIsAssistantMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated and self.request.user.is_admin or self.request.user.is_assistant:
            return True



