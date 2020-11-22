from rest_framework import routers
from veyron_kolesa.microservices.views import ServicesViewSet


router = routers.DefaultRouter()
router.register('', ServicesViewSet, base_name='microservices')

app_name = 'microservices'
urlpatterns = router.urls
