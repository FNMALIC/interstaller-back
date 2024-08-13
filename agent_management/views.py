# from rest_framework import viewsets
# from .models import User
# from .serializers import UserSerializer

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         role = self.request.query_params.get('role')
#         if role:
#             return self.queryset.filter(role=role)
#         return self.queryset


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from accounts.serializers import UserAccountSerializer
from .models import ChefAgent ,Agent, ChefManager, Client
from .serializers import ChefAgentSerializer, ChefManagerSerializer, ClientSerializer, CreateAgentSerializer ,AgentSerializer, CreateClientSerializer ,CreateChefAgentSerializer

from .permissions import IsChefAgent , IsAgent ,IsChefManager,IsClient


class ChefAgentViewSet(viewsets.ModelViewSet):
    queryset = ChefAgent.objects.all()
    serializer_class = ChefAgentSerializer
    permission_classes = [IsAuthenticated,IsChefAgent]

    @action(detail=True, methods=['post'])
    def create_agent(self, request, pk=None):
        chef_agent = self.get_object()
        serializer = CreateAgentSerializer(data=request.data, context={'chef_agent': chef_agent})
        serializer.is_valid(raise_exception=True)
        agent = serializer.save()
        return Response({"message": "Agent created successfully", "agent": UserAccountSerializer(agent.user).data})


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated,IsAgent]

    @action(detail=True, methods=['post'])
    def create_client(self, request, pk=None):
        agent = self.get_object()
        serializer = CreateClientSerializer(data=request.data, context={'agent': agent})
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        return Response({"message": "Client created successfully", "client": UserAccountSerializer(client.user).data})
    

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated , IsClient]

    @action(detail=True, methods=['post'])
    def pay_fee(self, request, pk=None):
        client = self.get_object()
        client.pay_monthly_fee()
        return Response({"message": "Monthly fee paid successfully"})


class ChefManagerViewSet(viewsets.ModelViewSet):
    queryset = ChefManager.objects.all()
    serializer_class = ChefManagerSerializer
    permission_classes = [IsAuthenticated ,IsChefManager]

    @action(detail=True, methods=['post'])
    def create_chef_agent(self, request, pk=None):
        chef_manager = self.get_object()
        serializer = CreateChefAgentSerializer(data=request.data, context={'chef_manager': chef_manager})
        serializer.is_valid(raise_exception=True)
        chef_agent = serializer.save()
        return Response({"message": "Chef Agent created successfully", "chef_agent": UserAccountSerializer(chef_agent.user).data})