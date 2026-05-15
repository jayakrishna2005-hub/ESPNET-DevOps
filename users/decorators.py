from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    """
    Decorator for views that checks whether a user has a particular role,
    raising PermissionDenied if the user does not have the required role.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator
