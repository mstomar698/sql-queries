import json
from django.core.management.base import BaseCommand
from datetime import datetime
from pytz import timezone


class Command(BaseCommand):
    help = 'Insert JSON data into the database'

    def handle(self, *args, **kwargs):
        try:
            with open('./static_data/management/commands/JSON/jsondata.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

                self.stdout.write(self.style.SUCCESS(
                    'Data loaded successfully'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('JSON file not found'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
