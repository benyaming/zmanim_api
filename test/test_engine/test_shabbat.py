from datetime import date, datetime as dt

import pytest

from zmanim_api.engine.shabbat import get_shabbat
from zmanim_api.api_helpers import HavdalaChoices
from ..consts import LAT, LNG, ZERO_ELEVATION, CL_OFFSET, HAVDALA, PY_DATE


@pytest.mark.shabbat
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

    resp = get_shabbat(LAT, LNG, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees, PY_DATE)
    assert resp.dict(exclude_none=True, by_alias=True) == expected


@pytest.mark.shabbat
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

    resp = get_shabbat(55.5, 37.7, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees,
                       date(2020, 6, 15))
    assert resp.dict(exclude_none=True, by_alias=True) == expected


@pytest.mark.shabbat
def test_shabbat_with_different_parsha():
    expected_1 = {
        'candle_lighting': dt.fromisoformat('2020-06-05T19:26:00+03:00'),
        'havdala': dt.fromisoformat('2020-06-06T20:26:00+03:00'),
        'settings': {
            'date': date.fromisoformat('2020-05-30'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0
        },
        'torah_part': 'behaalosecha',
        'late_cl_warning': False
    }
    expected_2 = {
        'candle_lighting': dt.fromisoformat('2020-06-05T19:41:00+03:00'),
        'havdala': dt.fromisoformat('2020-06-06T20:46:00+03:00'),
        'settings': {
            'date': date.fromisoformat('2020-05-30'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (37.7, 34.86),
            'elevation': 0
        },
        'torah_part': 'naso',
        'late_cl_warning': False
    }

    resp_1 = get_shabbat(LAT, LNG, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees, date.fromisoformat('2020-05-30'))
    resp_2 = get_shabbat(37.7, LNG, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees, date.fromisoformat('2020-05-30'))

    assert resp_1.dict(exclude_none=True, by_alias=True) == expected_1
    assert resp_2.dict(exclude_none=True, by_alias=True) == expected_2


@pytest.mark.shabbat
def test_shabbat_with_yomtov():
    expected_1 = {
        'candle_lighting': dt.fromisoformat('2020-05-29T19:22:00+03:00'),
        'havdala': dt.fromisoformat('2020-05-30T20:22:00+03:00'),
        'settings': {
            'date': date.fromisoformat('2020-05-29'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0
        },
        'torah_part': 'naso',
        'late_cl_warning': False
    }
    expected_2 = {
        'candle_lighting': dt.fromisoformat('2020-05-29T19:36:00+03:00'),
        'havdala': dt.fromisoformat('2020-05-30T20:41:00+03:00'),
        'settings': {
            'date': date.fromisoformat('2020-05-29'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (37.7, 34.86),
            'elevation': 0
        },
        'torah_part': 'shavuos',
        'late_cl_warning': False
    }
    expected_3 = {
        'candle_lighting': dt.fromisoformat('2020-04-10T18:53:00+03:00'),
        'havdala': dt.fromisoformat('2020-04-11T19:52:00+03:00'),
        'settings': {
            'date': date.fromisoformat('2020-04-10'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (37.7, 34.86),
            'elevation': 0
        },
        'torah_part': 'chol_hamoed_pesach',
        'late_cl_warning': False
    }

    resp_1 = get_shabbat(LAT, LNG, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees, date.fromisoformat('2020-05-29'))
    resp_2 = get_shabbat(37.7, LNG, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees, date.fromisoformat('2020-05-29'))
    resp_3 = get_shabbat(37.7, LNG, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees, date.fromisoformat('2020-04-10'))

    assert resp_1.dict(exclude_none=True, by_alias=True) == expected_1
    assert resp_2.dict(exclude_none=True, by_alias=True) == expected_2
    assert resp_3.dict(exclude_none=True, by_alias=True) == expected_3
