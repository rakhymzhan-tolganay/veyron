from django.core.management.base import BaseCommand
from veyron_kolesa.microservices.models import Service
import sys
# from veyron_kolesa.parser.advert_links import main
from veyron_kolesa.parser.scrape_car import main
# from veyron_kolesa.parser.export_scv import export


class Command(BaseCommand):

    def handle(self, *args, **options):
        sys.stdout.write("This is function handle in class Command in file scrapper\n")
        sys.stdout.write("This is function handle in class Command in file scrapper\n")
        sys.stdout.write("Main function is starting!\n")
        # export()
        main()
        sys.stdout.write("End of scraper page\n")
        # main()
