from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('ALUMNI', 'Alumni'),
        ('USER', 'Normal User')
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_default_role():
        return UserRole.objects.get(name='USER').id
    
def get_default_user_role():
    return UserRole.get_default_role() 

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True,null=True)
    bio = models.TextField(null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, related_name='users')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def get_role_display(self):
        return self.role.name if self.role else 'No Role'

    @property
    def is_admin(self):
        return self.role and self.role.name == 'ADMIN'

    @property
    def is_alumni(self):
        return self.role and self.role.name == 'ALUMNI' 