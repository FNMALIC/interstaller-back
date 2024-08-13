from django.urls import path, include
from rest_framework.routers import DefaultRouter
from agent_management.views import (
    ChefAgentViewSet,
    AgentViewSet,
    ClientViewSet,
    ChefManagerViewSet
)
router = DefaultRouter()
router.register(r'chef_agents', ChefAgentViewSet, basename='chef_agent')
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'chef_managers', ChefManagerViewSet, basename='chef_manager')


urlpatterns = [
    path('', include(router.urls)),
    # path('api/register-agent-manager/', RegisterAgentManagerView.as_view(), name='register-agent-manager'),
]