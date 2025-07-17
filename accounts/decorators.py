from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role != required_role:
                return redirect('403')  # Create a 403.html or redirect elsewhere
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

mentor_required = role_required('mentor')
mentee_required = role_required('mentee')
admin_required = role_required('admin')
