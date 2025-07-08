from django.core.management.base import BaseCommand
from scraper.utils import scrape_fincen

class Command(BaseCommand):
    help = 'Scrapes the FinCEN special measures table and updates the database.'

    def handle(self, *args, **kwargs):
        result = scrape_fincen()
        self.stdout.write(self.style.SUCCESS(
            f"Scraping done. Added: {len(result['added'])}, Removed: {len(result['removed'])}"
        ))
