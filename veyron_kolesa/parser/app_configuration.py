# Kolesa models
from veyron_kolesa.parser.models import Autosalon, Car


class AppConfig:
    # DT_AVTOSALON = 'avtosalon'
    DT_LEGKOVYE = 'legkovye'


    URLS_CORRESPOND_MODELS = {
    #     'avtosalon/': DT_AVTOSALON,
                              'cars/': DT_LEGKOVYE
    }

    CORRESPOND_MODELS = {
        # DT_AVTOSALON: Autosalon,
                         DT_LEGKOVYE: Car
                         }

    MODELS = [DT_LEGKOVYE,
              # DT_AVTOSALON,
              ]
