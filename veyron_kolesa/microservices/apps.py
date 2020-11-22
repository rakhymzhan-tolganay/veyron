from django.apps import AppConfig

services = None


class MicroservicesConfig(AppConfig):
    name = 'veyron_kolesa.microservices'

    # def ready(self):
    #     try:
    #         from veyron_kolesa.microservices.models import Service
    #
    #         global services
    #         services = Service.objects.all()
    #     except:
    #         pass
