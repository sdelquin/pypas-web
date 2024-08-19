from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Reset admin password'

    def handle(self, *args, **options):
        admin = User.objects.get(username='admin')
        admin.set_password('admin')
        admin.save()
