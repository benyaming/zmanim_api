from datetime import date, datetime as dt

from zmanim_api.engine.shabbat import get_shabbat
from zmanim_api.api_helpers import HavdalaChoises
from ..consts import LAT, LNG, ZERO_ELEVATION, CL_OFFSET, HAVDALA, PY_DATE


def test_regular_shabbat():
    expected = {
        'candle_lighting': dt.fromisoformat('2020-04-17T18:53:00+03:00'),
        'havdala': dt.fromisoformat('2020-04-18T19:49:00+03:00'),
        'settings': {
            'date': date.fromisoformat('2020-04-15'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0
        },
        'torah_part': 'shemini',
        'late_cl_warning': False
    }

    resp = get_shabbat(LAT, LNG, ZERO_ELEVATION, CL_OFFSET, HavdalaChoises.tzeis_8_5_degrees,  PY_DATE)
    assert resp.dict(exclude_none=True, by_alias=True) == expected


def test_shabbat_with_late_cl_warning():
    expected = {
        'candle_lighting': dt.fromisoformat('2020-06-19T20:57:00+03:00'),
        'havdala': dt.fromisoformat('2020-06-20T22:55:00+03:00'),
        'settings': {
            'date': date.fromisoformat('2020-06-15'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (55.5, 37.7),
            'elevation': 0
        },
        'torah_part': 'shelach',
        'late_cl_warning': True
    }

    resp = get_shabbat(55.5, 37.7, ZERO_ELEVATION, CL_OFFSET, HavdalaChoises.tzeis_8_5_degrees,
                       date(2020, 6, 15))
    assert resp.dict(exclude_none=True, by_alias=True) == expected
