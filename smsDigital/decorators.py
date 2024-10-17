from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user_roles = request.user.groups.values_list('name', flat=True)
            if set(user_roles).intersection(allowed_roles):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("<h1>Forbidden</h1>")
        return _wrapped_view
    return decorator