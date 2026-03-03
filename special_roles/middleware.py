from .models import UserSpecialRole

class SpecialRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.special_role = None

        if request.user.is_authenticated:
            try:
                role_obj = UserSpecialRole.objects.get(user=request.user)
                request.special_role = role_obj.role
            except UserSpecialRole.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
