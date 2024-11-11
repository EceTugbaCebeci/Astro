from django.core.management.base import BaseCommand
from natalcharts.utils import update_monthly_comments

class Command(BaseCommand):
    help = 'Update probabilities comments'

    def handle(self, *args, **kwargs):
        update_monthly_comments()
        self.stdout.write(self.style.SUCCESS('Successfully updated probabilities comments'))
