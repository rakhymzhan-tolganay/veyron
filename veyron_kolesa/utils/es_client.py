from django.conf import settings
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch_dsl import analyzer

es_client = Elasticsearch(
    hosts=[settings.ELASTICSEARCH_HOST],
    connection_class=RequestsHttpConnection
)

native_russian = analyzer('russian')
