import os
import sys
import redis
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from .redisqueue import RedisQueue
from celery.schedules import crontab
import time
from celery.task import periodic_task
from .proxy import change_proxy, proxy, useragent, get_variable
from veyron_kolesa.parser.models import Autosalon, Car
from veyron_kolesa.parser.export_scv import models_id
from veyron_kolesa.parser.app_configuration import AppConfig as appconf


class MainScrape:
    print("MainScrape class")
    soup = None

    def __init__(self):
        self.proxy = proxy()
        self.useragent = useragent()
        self.base_url = "https://kolesa.kz"
        self.func_list = {
            # appconf.DT_AVTOSALON: self.put_db_autosalon,
            appconf.DT_LEGKOVYE: self.put_db_car
                      }

    def set_help_str_model(self, help_model_name):
        self.help_model_name = help_model_name

    # Take phone number from 'Показать телефон'
    def get_phone(self, id):
        link = "a/ajaxPhones/"
        url = os.path.join(self.base_url, link)
        params = {'id': id}
        request = change_proxy(url, self.proxy, self.useragent, params)
        return request.json()

    # def put_db_autosalon(self, link_id, characteristics, advert_title, url, phones_data, city, price, text_data,
    #                      list_of_pictures):
    #     # scrape own fields of this model
    #     # soup = self.soup
    #     address = characteristics["Адрес"] if "Адрес" in characteristics else "No such data"
    #     web_site = characteristics["Адрес сайта"] if "Адрес сайта" in characteristics else "No such data"
    #     time = self.soup.find_all('ul', {'class': 'shop-mode'})
    #     timetable = ""
    #     for i in range(len(time)):
    #         timetable += time[i].get_text() + "\n"
    #     autosalon = Autosalon(link_id=link_id, advert_title=advert_title, url=url, phones=phones_data, city=city,
    #                           address=address, website_address=web_site, timetable=timetable,
    #                           description_text=text_data, images=list_of_pictures)
    #     autosalon.save()

    def put_db_car(self, link_id, characteristics, advert_title, url, phones_data, city, price, text_data,
                   list_of_pictures):
        q = get_variable(url, "window.digitalData")
        pubDate = q['product']['publicationDate'].split("T")[0]
        appliedPaidServices = []
        if 'appliedPaidServices' in q['product']:
            appliedPaidServices = q['product']['appliedPaidServices']
        print(appliedPaidServices)

        brand = (self.soup.find('span', {'itemprop': 'brand'})).get_text()
        model = (self.soup.find('span', {'itemprop': 'name'})).get_text()

        in_model = brand + " " + model
        car_id = 0
        if in_model in models_id:
            print("THIS MODEL EXIST IN OUR DATA")
            print(models_id.get(in_model))
            car_id = models_id.get(in_model)

        year = int((self.soup.find('span', {'class': 'year'})).get_text())
        body = characteristics["Кузов"] if "Кузов" in characteristics else "No such data"
        engine_volume = characteristics["Объем двигателя, л"] if "Объем двигателя, л" in characteristics else None
        for_mileage = characteristics["Пробег"] if "Пробег" in characteristics else None
        mileage = int("".join(
            [for_mileage[i] for i in range(len(for_mileage)) if for_mileage[i].isdigit()])) if for_mileage else None
        gearbox = characteristics["Коробка передач"] if "Коробка передач" in characteristics else "No such data"
        wheel = characteristics["Руль"] if "Руль" in characteristics else "No such data"
        color = characteristics["Цвет"] if "Цвет" in characteristics else "No such data"
        drive = characteristics["Привод"] if "Привод" in characteristics else "No such data"
        custom_cleared = characteristics["Растаможен"] if "Растаможен" in characteristics else None
        vin = characteristics["Растоможен"] if "" in characteristics else "No such data"

        # for_avtosalon_url = self.soup.find('a', {'class': 'shop__info-title'})
        # avtosalon_url = os.path.join("https://kolesa.kz", for_avtosalon_url["href"][1:]) if for_avtosalon_url else \
        #     "No autosalon"
        # try:
        #     avtosalon = Autosalon.objects.get(url=avtosalon_url)
        # except Autosalon.DoesNotExist:
        #     avtosalon = None

        car = Car(link_id=link_id, advert_title=advert_title, url=url, phones=phones_data, city=city, price=price,
                  brand=brand, car_id=car_id, pubDate=pubDate, appliedPaidServices=appliedPaidServices,
                  model=model, year=year, body=body, engine_volume=engine_volume, mileage=mileage, gearbox=gearbox,
                  description_text=text_data, wheel=wheel, color=color, drive=drive,
                  custom_cleared=custom_cleared, vin=vin,
                  # avtosalon_name=avtosalon, avtosalon_url=avtosalon_url,
                  images=list_of_pictures)
        car.save()


    # Take static fields of page
    def scrape_static_fields(self, link):
        sys.stdout.write("I am heeereeeeeeee-----------------")
        link = link[1:]
        # link = "a/show/{}".format(id)
        id = int(link.split('/')[2])
        url = os.path.join(self.base_url, link)
        request = change_proxy(url, self.proxy, self.useragent)
        self.soup = BeautifulSoup(request.content, "html.parser")
        sys.stdout.write("Url:  ")
        sys.stdout.write(url)

        # get title of advert
        advert_title = self.soup.find('h1', {'class': 'offer__title'})
        if advert_title:
            advert_title = advert_title.get_text().strip()

        price = self.soup.find('div', {'class': 'offer__price'})
        if price:
            price = int(("".join(price.get_text().split()))[:-1])

        # get all characteristics
        characteristics = {}
        keys = self.soup.find_all('dt', {'class': 'value-title'})
        try:
            keys = [keys[i]["title"] for i in range(len(keys))]
        except:
            keys = [(keys[i].get_text()).replace("\n", "").replace("\xa0", "") for i in range(len(keys))]
        for_values = self.soup.find_all('dd', {'class': 'value'})
        values = []
        for i in range(len(for_values)):
            if "br" in str(for_values[i]):
                for_val_arr = (str(for_values[i]).split("<br/>"))
                value_arr = [i.replace('<dd class="value">\n', "").replace(" ", "").replace("</dd>", "")
                             for i in for_val_arr]
                values.append(value_arr)
            else:
                values.append(for_values[i].get_text().replace("\n", "").replace("  ", ""))
        for i in range(len(keys)):
            characteristics[keys[i]] = values[i]

        # get city
        city = characteristics["Город"]

        # get all phones of seller
        phones_data = (self.get_phone(id))['phones']
        sys.stdout.write("Phooooone daaaaataaaaa:   ")
        print(phones_data)
        if phones_data is None:
            phones_data = ["No phones"]

        # get description text of advert
        text_data = self.soup.find('div', {'class': 'offer__description'})
        if text_data:
            text_data = " ".join(text_data.get_text().split("\n"))
        sys.stdout.write(text_data)

        # get all urls of photos
        picture_soup = self.soup.find_all('a', {"class": "gallery__thumb-image js__gallery-thumb-link"})
        list_of_pictures = list()
        try:
            for i in range(len(picture_soup)):
                data_photo_url = picture_soup[i]["href"]
                list_of_pictures.append(data_photo_url)
        except Exception as e:
            sys.stdout.write("Does not contain any images")
            sys.stdout.write(str(e))
        if len(list_of_pictures) == 0:
            list_of_pictures.append("no images")

        # sys.stdout.write("I ended to get data from the site, now i will put it to database")
        # Put data into db
        self.func_list.get(self.help_model_name, None)(id, characteristics, advert_title, url, phones_data, city, price,
                                                       text_data, list_of_pictures)


@periodic_task(run_every=crontab(hour=3, minute=00, day_of_week='tue,fri'))
def main():
    print("Print from Scrape main")
    ms = MainScrape()
    redis_shops = redis.Redis(host='redis', port=6379, db=0)
    rediska = redis.Redis(host='redis', port=6379, db=1)
    redis_list = [redis_shops, rediska]
    for rediska in redis_list:
        for link_id in rediska.keys():
            link = os.path.join('/a/show', link_id.decode("utf-8"))
            try:
                help_model_name = rediska.get(link_id.decode("utf-8"))
                print("Before first ERRRR...")
                if_exists = appconf.CORRESPOND_MODELS[help_model_name.decode("utf-8")].objects.filter \
                    (link_id=link_id.decode("utf-8")).exists()
            except Exception as e:
                if_exists = True
                print("First ERRRRRRRR......", e)
            if if_exists:
                sys.stdout.write("It exists in db! And i am in main func!!!!!")
            else:
                sys.stdout.write("It doesn't exist in db! And i am in main func!!!!")
                try:
                    ms.set_help_str_model(help_model_name.decode("utf-8"))
                    ms.scrape_static_fields(link)
                    sys.stdout.write("---------Ended 1 page-----------")
                except Exception as e:
                    sys.stdout.write("*-*-*-*-*-*-*- ERR: ")
                    sys.stdout.write(str(e))

    sys.stdout.write("I ended with parsing and putting it to database")
    # sys.stdout.write(clean_redis.qsize())
    sys.stdout.write("I ended with parsing and putting it to database")


if __name__ == "__main__":
    main()
