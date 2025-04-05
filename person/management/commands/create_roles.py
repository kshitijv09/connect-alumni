from django.core.management.base import BaseCommand
from person.models import UserRole

class Command(BaseCommand):
    help = 'Creates default user roles'

    def handle(self, *args, **kwargs):
        roles = ['ADMIN', 'ALUMNI', 'USER']
        created_roles = []
        
        for role_name in roles:
            role, created = UserRole.objects.get_or_create(name=role_name)
            if created:
                created_roles.append(role_name)
        
        if created_roles:
            self.stdout.write(self.style.SUCCESS(f'Successfully created roles: {", ".join(created_roles)}'))
        else:
            self.stdout.write(self.style.SUCCESS('All roles already exist')) 