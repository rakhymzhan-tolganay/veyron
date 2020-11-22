from django.urls import path
from rest_framework import routers

from veyron_kolesa.users.views import UserListDebug

router = routers.DefaultRouter()

app_name = "users"
urlpatterns = [
    path('all/', UserListDebug.as_view())
]

urlpatterns += router.urls
