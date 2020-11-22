from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class StaticFields(models.Model):
    link_id = models.IntegerField(default=0)
    advert_title = models.CharField(max_length=350)
    url = models.URLField(verbose_name="Url")
    city = models.CharField(max_length=200, blank=True, null=True)
    phones = ArrayField(models.CharField(max_length=20, blank=True, null=True, help_text='Phone number'))
    description_text = models.TextField(null=True, blank=True)
    images = ArrayField(models.TextField())

    class Meta:
        abstract = True

    def __str__(self):
        return self.advert_title


class ShopStatic(StaticFields):

    address = models.CharField(max_length=300, blank=True, null=True)
    timetable = models.CharField(max_length=400, blank=True, null=True)  # График работы

    class Meta:
        abstract = True


class Autosalon(ShopStatic):  # Автосалон
    website_address = models.URLField(verbose_name="website address")  # Адрес сайта


class Car(StaticFields):  # Легковые
    car_id = models.IntegerField(blank=True, null=True)
    pubDate = models.DateField(blank=True, null=True)
    appliedPaidServices = ArrayField(models.CharField(max_length=50, blank=True, null=True),default=list)
    brand = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True, default=0)
    price = models.IntegerField(blank=True, null=True, default=0)
    body = models.CharField(max_length=200, blank=True, null=True)  # кузов
    engine_volume = models.CharField(max_length=200, blank=True, null=True)  # объем двигателя
    mileage = models.IntegerField(blank=True, null=True, default=0)  # пробег
    gearbox = models.CharField(max_length=200, blank=True, null=True)  # Коробка передач
    wheel = models.CharField(max_length=200, blank=True, null=True)  # Руль
    color = models.CharField(max_length=200, blank=True, null=True)  # цвет
    drive = models.CharField(max_length=200, blank=True, null=True)  # Привод
    custom_cleared = models.CharField(max_length=3, blank=True, null=True)  # Растоможен
    vin = models.CharField(max_length=200, blank=True, null=True)  # Вин
    avtosalon_name = models.ForeignKey(Autosalon, null=True, blank=True, related_name="car", on_delete=models.CASCADE)  # название автосалона
    avtosalon_url = models.URLField(verbose_name="Autosalon url")  # ссылка автосалона
