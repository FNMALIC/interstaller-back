from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from workstations.views import WorkstationViewSet 
        # WorkstationMembershipViewSet
# from agent_management.views import AgentManagerViewSet, AgentViewSet, ActivationViewSet, AccountBalanceViewSet, RegisterAgentManagerView


router = DefaultRouter()
# router.register(r'workstations', WorkstationViewSet)
# router.register(r'workstation_membership', WorkstationMembershipViewSet)
# router.register(r'agent-managers', AgentManagerViewSet)
# router.register(r'agents', AgentViewSet)
# router.register(r'activations', ActivationViewSet)
# router.register(r'account-balances', AccountBalanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api/register-agent-manager/', RegisterAgentManagerView.as_view(), name='register-agent-manager'),
]