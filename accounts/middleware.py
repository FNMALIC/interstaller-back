from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from agent_management.models import ChefAgent, Agent

from django.shortcuts import redirect

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check user role and restrict access as needed
        if request.user.is_authenticated:
            if request.user.role == 'client' and request.path.startswith('/admin/'):
                return redirect('/not-allowed/')  # Redirect clients away from admin URLs
        
        response = self.get_response(request)
        return response


class CheckActivityStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only check activity status if the user is logged in
        if request.user.is_authenticated:
            if request.user.role == 'chef_agent':
                self.check_chef_agent_activity(request.user)
            elif request.user.role == 'agent':
                self.check_agent_activity(request.user)
        
        return response

    def check_chef_agent_activity(self, user):
        try:
            chef_agent = ChefAgent.objects.get(user=user)
            # Check if the last activation was more than 2 days ago
            if chef_agent.last_activation_date and (timezone.now() - chef_agent.last_activation_date) > timedelta(days=2):
                # Set the account to inactive if not active
                user.is_active = False
                user.save()
        except ChefAgent.DoesNotExist:
            raise PermissionDenied("ChefAgent not found")

    def check_agent_activity(self, user):
        try:
            agent = Agent.objects.get(user=user)
            # Check if the last activation was more than 1 day ago
            if agent.last_activation_date and (timezone.now() - agent.last_activation_date) > timedelta(days=1):
                # Set the account to inactive if not active
                user.is_active = False
                user.save()
        except Agent.DoesNotExist:
            raise PermissionDenied("Agent not found")
