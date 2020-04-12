from datetime import date

from zmanim.limudim.calculators.daf_yomi_bavli import DafYomiBavli


def get_daf_yomi(date_: date = None) -> dict:
    daf_yomi = DafYomiBavli().limud(date_ or date.today())
    daf_yomi_data = {
        'masehet': daf_yomi.unit.components[0][0],
        'daf': daf_yomi.unit.components[0][1]
    }
    return daf_yomi_data
