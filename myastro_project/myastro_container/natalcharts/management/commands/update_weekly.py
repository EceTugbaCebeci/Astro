from django.core.management.base import BaseCommand
from natalcharts.utils import update_weekly_comments

class Command(BaseCommand):
    help = 'Update probabilities comments'

    def handle(self, *args, **kwargs):
        update_weekly_comments()
        self.stdout.write(self.style.SUCCESS('Successfully updated probabilities comments'))
