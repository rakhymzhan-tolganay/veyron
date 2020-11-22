from requests import Request, Session

from django.db import models


class Service(models.Model):
    CAPS = 'caps'

    name = models.CharField(
        unique=True,
        editable=False,
        max_length=100,
        help_text="Name of the service."
    )

    host = models.URLField(
        unique=True,
        editable=False,
        help_text="Host of the service. Ex. auth.example.com"
    )

    url = models.URLField(
        editable=True,
        help_text="URL of the proxy to the service, Ex. traefik IP address"
    )

    objects = models.Manager()

    class Meta:
        ordering = ['name', 'host']

    def __str__(self):
        return '{name} ({host})'.format(name=self.name, host=self.host)

    def __unicode__(self):
        return '{name} ({host})'.format(name=self.name, host=self.host)

    def remote_call(self, method, api='', headers=None, cookies=None, data=None, request_kw=None, session_kw=None):
        if request_kw is None:
            request_kw = {}

        if session_kw is None:
            session_kw = {}

        if headers is None:
            headers = {}

        session = Session()

        url = self.url
        host = self.host if self.host[-1] != '/' else self.host[:-1]

        headers.update({
            'Host': host
        })

        api_endpoint = api if api[0] != '/' else api[1:]

        url = '{url}/{api_endpoint}'.format(url=url, api_endpoint=api_endpoint)

        request = Request(method=method.upper(), url=url, data=data, **request_kw)
        prepared_request = session.prepare_request(request)

        prepared_request.headers.update(headers)

        if data is not None:
            prepared_request.data = data

        if cookies is not None:
            session.cookies.update(cookies)

        response = session.send(request=prepared_request, **session_kw)

        return response
