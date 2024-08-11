from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, role='', sex='', interrest=None, city=None, business=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        print(role)
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            role=role,
            sex=sex,
            interrest=interrest,
            city=city,
            business=business,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, role='admin', **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('agent_manager', 'Chief_Agent'),
        ('agent', 'Agent'),
        ('client', 'Client'),
    )
    SEX_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=None, null=True)
    sex = models.CharField(max_length=15, choices=SEX_CHOICES, default=None, null=True)
    interest = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    business = models.CharField(max_length=20, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        permissions = [
            ("access_admin_routes", "Can access admin routes"),
            ("access_user_routes", "Can access user routes"),
        ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role in ['admin', 'chef_agent']:
            admin_group, _ = Group.objects.get_or_create(name='admins')
            admin_group.user_set.add(self)
        else:
            user_group, _ = Group.objects.get_or_create(name='users')
            user_group.user_set.add(self)

class UserActionLog(models.Model):
    ACTION_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    )
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.timestamp}"
