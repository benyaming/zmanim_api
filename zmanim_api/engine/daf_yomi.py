from datetime import date

from zmanim.limudim.calculators.daf_yomi_bavli import DafYomiBavli

from ..models import DafYomi, SimpleSettings


def get_daf_yomi(date_: date = None) -> DafYomi:
    daf_yomi = DafYomiBavli().limud(date_ or date.today())
    daf_yomi_data = {
        'masehet': daf_yomi.unit.components[0][0],
        'daf': daf_yomi.unit.components[0][1]
    }
    settings = SimpleSettings(date=date_)
    return DafYomi(settings=settings, **daf_yomi_data)
