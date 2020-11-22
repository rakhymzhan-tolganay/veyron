import js2py
import requests
from bs4 import BeautifulSoup



def proxy():
    proxies = open('veyron_kolesa/parser/ip/proxies.txt').read().split('\n')
    while True:
        for proxy in proxies:
            yield proxy


def useragent():
    useragents = open('veyron_kolesa/parser/ip/useragents.txt').read().split('\n')
    while True:
        for useragent in useragents:
            yield useragent


def change_proxy(url, gen_proxy, gen_useragent, params={}):
    check = True

    while True:
        if not check:
            break

        _proxy = {'http': 'http://' + next(gen_proxy)}
        _useragent = {"X-Requested-With": "XMLHttpRequest", 'User-Agent': next(gen_useragent)}

        try:
            r = requests.get(url, params=params, headers=_useragent, proxies=_proxy, timeout=3)
            check = False
        except:
            continue

    return r

def get_variable(url, var):
    _proxy = {'http': 'http://' + "134.209.36.113:3128"}
    _useragent = {'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)"}
    response = requests.get(url, headers=_useragent, proxies=_proxy)
    soup = BeautifulSoup(response.content, "html.parser")
    data = soup.find_all("script")
    script = 'return mydata;'
    for i in data:
        if var in i.text:
            x = i.text.split("};")
            if "var" not in x[0]:
                x[0] = x[0].replace(var, "var mydata")
            else:
                x[0] = x[0].replace(var, "mydata")
            if "BACKEND." in x[0]:
                x[0] = x[0].replace("BACKEND.", "")
            s = "function f() { " + x[0] + "};" + script + " } "
            f = js2py.eval_js(s)
            obj = eval(str(f()).replace("\'", "\""))
            return obj
