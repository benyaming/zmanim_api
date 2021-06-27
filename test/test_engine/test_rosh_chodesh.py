from datetime import date, datetime as dt

from zmanim_api.engine.rosh_chodesh import get_next_rosh_chodesh
from ..consts import PY_DATE


def test_regular_rosh_chodesh():
    expected = {
        'settings': {'date': date.fromisoformat('2020-04-15')},
        'month_name': 'iyar',
        'days': [date.fromisoformat('2020-04-24'), date.fromisoformat('2020-04-25')],
        'duration': 2,
        'molad': (dt.fromisoformat('2020-04-22T22:58'), 12)
    }

    actual = get_next_rosh_chodesh(PY_DATE)
    assert actual.dict(exclude_none=True, by_alias=True) == expected


def test_rosh_chodesh_before_rosh_hashana():
    expected = {
        'settings': {'date': date.fromisoformat('2020-09-30')},
        'month_name': 'cheshvan',
        'days': [date.fromisoformat('2020-10-18'), date.fromisoformat('2020-10-19')],
        'duration': 2,
        'molad': (dt.fromisoformat('2020-10-17T03:23'), 0)
    }

    actual = get_next_rosh_chodesh(date(2020, 9, 1))
    assert actual.dict(exclude_none=True, by_alias=True) == expected
