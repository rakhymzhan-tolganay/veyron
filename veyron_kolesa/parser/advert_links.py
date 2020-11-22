import os
import sys
import redis
from celery import Celery
from bs4 import BeautifulSoup
from celery import shared_task
from django.utils import timezone
from celery.schedules import crontab
from celery.task import periodic_task
from veyron_kolesa.parser.proxy import proxy, useragent, change_proxy

from veyron_kolesa.parser.app_configuration import AppConfig as appconf

base_url = "https://kolesa.kz"
gen_proxy = proxy()
gen_useragent = useragent()


def get_transport_advert_links(url_of_page, model_name):
    print("IN function")
    url = os.path.join(base_url, url_of_page)
    # changes IP
    page = change_proxy(url, gen_proxy, gen_useragent)
    redis_shops = redis.Redis(host='redis', port=6379, db=0)
    rediska = redis.Redis(host='redis', port=6379, db=1)
    soup2 = BeautifulSoup(page.content, "html.parser")
    # gets div class in which have all regions
    cities = soup2.find('ul', {'class': 'cross-links-list cross-links__columns cross-links__columns--2'})
    ahref = cities.find_all('a')
    region_data_list = list()
    if (len(url_of_page.split('/')) == 2):
        gorod = 2
    else:
        gorod = 3
    for j in ahref:
        link_city = j['href']
        city = str(link_city.split('/')[gorod])
        region_data_list.append(city)

    # print("Region data list:   ", region_data_list)

    for region in range(len(region_data_list)):
        sys.stdout.write("And another loop has been started\n")
        for_region_url = region_data_list[region] + "/"
        url2 = os.path.join(url, for_region_url)
        page2 = change_proxy(url2, gen_proxy, gen_useragent)
        soup3 = BeautifulSoup(page2.content, "html.parser")

        # button "Показать n объявлении"
        text_with_quantity = soup3.find("span", {"class": "label js__search-form-submit-value"})
        splited_text = text_with_quantity.get_text().split(" ")
        count = ""
        # get number which is quantity of advertisements
        for word_index in range(len(splited_text)):
            if splited_text[word_index].isdigit():
                count += splited_text[word_index]
        try:
            count_result = int(count)
        except:
            count_result = 0
        print("count result is:  ", count_result)

        for page_index in range(count_result // 20 + 1):
            try:
                page = {'page': page_index + 1}
                page3 = change_proxy(url2, gen_proxy, gen_useragent, params=page)
                soup = BeautifulSoup(page3.content, "html.parser")
                cars = soup.find_all('a', {'class': "list-link ddl_product_link"})
                # interval of for loop is 2, because there are 2 links of one page
                for cars_index in range(1, len(cars), 2):
                    sys.stdout.write("I am heeeeereeeeeee!")
                    sys.stdout.write(cars[cars_index].get_text())
                    for_car_url = cars[cars_index]["href"]
                    car_url = os.path.join(base_url, for_car_url[1:])
                    print("car url:     ", car_url)
                    # car_url = /a/show/id
                    link_id = int(for_car_url[1:].split("/")[2])
                    print("id:   ", link_id)
                    if redis_shops.exists(link_id) == 0:
                        redis_shops.set(link_id, model_name)
                        print("Redis db doesn't exist and i putted to redis")
                    # c
                    else:
                        print("It EXISTS in REDIS DB, so i can't add it to db")

                sys.stdout.write("STEP: ")
                sys.stdout.write(str(page_index + 1))
                sys.stdout.write("LEN: ")
                sys.stdout.write(str(len(cars) / 2))
            except Exception as e:
                print("*-*-*-*-*-*-*- ERR: ", e)
                sys.stdout.write("There is no adverts in this city!")


@periodic_task(run_every=crontab(hour=23, minute=59, day_of_week='mon,thu'))
def main():
    print(9)
    now = timezone.now()
    for link, model_name in appconf.URLS_CORRESPOND_MODELS.items():
        get_transport_advert_links(link, model_name)
        print(f"Time is -------{now}")


if __name__ == "__main__":
    main()
