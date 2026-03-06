from .models import UserSpecialRole
from special_roles.models import UserSpecialRole

class SpecialRoleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.special_role = None

        if request.user.is_authenticated:

            role = UserSpecialRole.objects.filter(user=request.user).first()

            if role:
                request.special_role = role.role

        response = self.get_response(request)
        return response