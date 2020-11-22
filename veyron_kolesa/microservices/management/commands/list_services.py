from django.core.management.base import BaseCommand
from veyron_kolesa.microservices.models import Service


class Command(BaseCommand):
    help = 'List status of the services'

    def formatter(self, status):
        if status:
            return self.style.SUCCESS('available')

        if status is not None and not status:
            return self.style.ERROR('unavailable')

        return self.style.WARNING('unknown')

    def handle(self, *args, **options):
        services = Service.objects.all()

        for service in services.order_by('is_available'):
            self.stdout.write('{name} service is {status}'.format(
                name=service.name, status=self.formatter(service.is_available)
            ))
