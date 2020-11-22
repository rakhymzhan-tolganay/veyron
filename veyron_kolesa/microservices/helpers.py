import json
import os
import tempfile
import requests

from veyron_kolesa.microservices.models import Service


def refresh_service_configuration_data(configuration_file):
    if not os.path.isfile(configuration_file):

        configuration = requests.get(configuration_file).content

        _, configuration_file = tempfile.mkstemp(suffix='.json')

        f = open(configuration_file, "wb+")
        f.write(configuration)
        f.close()

    # call_command('loaddata', os.path.abspath(configuration_file))
    f = open(configuration_file, "r")
    data = json.loads(f.read())

    for i in data:
        pk = i['pk']
        name = i['fields']['name']
        url = i['fields']['url']
        host = i['fields']['host']

        print(i)

        if Service.objects.filter(id=pk).exists():
            service = Service.objects.get(id=pk)
            if not any([service.name == name, service.url == url, service.host == host]):
                service.delete()
            else:
                continue

        Service.objects.create(id=pk, name=name, url=url, host=host)
