from django.urls import path
from veyron_kolesa.parser import views

app_name = 'parser'

urlpatterns = [
    path('advert-list/', views.ResultView.as_view()),
]
