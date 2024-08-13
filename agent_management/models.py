from django.db import models
from accounts.models import UserAccount


class ChefAgent(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    activation_counter = models.IntegerField(default=0)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_activation_date = models.DateTimeField(null=True, blank=True)

    def create_agent(self, username, email, password):
        if self.agent_set.count() < 30:
            agent_user = UserAccount.objects.create_user(username=username, email=email, password=password, role='agent')
            Agent.objects.create(user=agent_user, chef_agent=self)
        else:
            raise ValueError("Maximum number of agents reached.")

    def reset_activation_counter(self):
        self.activation_counter = 0
        self.save()

    def update_account_balance(self, amount):
        self.account_balance += amount
        self.save()


class Agent(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    chef_agent = models.ForeignKey(ChefAgent, on_delete=models.CASCADE)
    activation_counter = models.IntegerField(default=0)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_activation_date = models.DateTimeField(null=True, blank=True)

    def create_client(self, username, email, password):
        client_user = UserAccount.objects.create_user(username=username, email=email, password=password, role='client')
        Client.objects.create(user=client_user, agent=self)

    def reset_activation_counter(self):
        self.activation_counter = 0
        self.save()

    def update_account_balance(self, amount):
        self.account_balance += amount
        self.save()

class Client(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    monthly_fee_paid = models.BooleanField(default=False)

    def pay_monthly_fee(self):
        if not self.monthly_fee_paid:
            self.monthly_fee_paid = True
            self.save()
            # Update Agent and ChefAgent balances
            self.agent.update_account_balance(300)
            self.agent.chef_agent.update_account_balance(200)


class ChefManager(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def create_chef_agent(self, username, email, password):
        chef_agent_user = UserAccount.objects.create_user(username=username, email=email, password=password, role='chef_agent')
        ChefAgent.objects.create(user=chef_agent_user)
    
    def update_account_balance(self, amount):
        self.account_balance += amount
        self.save()
