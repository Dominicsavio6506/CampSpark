def is_role(request, role_code):
    return getattr(request, 'special_role', None) == role_code
