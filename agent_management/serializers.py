from rest_framework import serializers
from .models import *
from accounts.serializers import UserAccountSerializer

class ChefAgentSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = ChefAgent
        fields = ['id', 'user', 'activation_counter', 'account_balance', 'last_activation_date']

class AgentSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    chef_agent = ChefAgentSerializer()

    class Meta:
        model = Agent
        fields = ['id', 'user', 'chef_agent', 'activation_counter', 'account_balance', 'last_activation_date']


class AgentSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    chef_agent = ChefAgentSerializer()

    class Meta:
        model = Agent
        fields = ['id', 'user', 'chef_agent', 'activation_counter', 'account_balance', 'last_activation_date']


class ClientSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    agent = AgentSerializer()

    class Meta:
        model = Client
        fields = ['id', 'user', 'agent', 'monthly_fee_paid']


class ChefManagerSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = ChefManager
        fields = ['id', 'user', 'account_balance']

class CreateAgentSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        chef_agent = self.context['chef_agent']
        return chef_agent.create_agent(**validated_data)


class CreateClientSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        agent = self.context['agent']
        return agent.create_client(**validated_data)

class CreateChefAgentSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        chef_manager = self.context['chef_manager']
        return chef_manager.create_chef_agent(**validated_data)
