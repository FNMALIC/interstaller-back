from django.utils.deprecation import MiddlewareMixin
from .models import UserActionLog

class UserActionLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.role == 'employee':
            if request.method == 'POST':
                action = 'create' if 'add' in request.path else 'update' if 'change' in request.path else 'delete'
                UserActionLog.objects.create(user=request.user, action=action)
            elif request.method == 'GET':
                if 'login' in request.path:
                    UserActionLog.objects.create(user=request.user, action='login')
                elif 'logout' in request.path:
                    UserActionLog.objects.create(user=request.user, action='logout')
