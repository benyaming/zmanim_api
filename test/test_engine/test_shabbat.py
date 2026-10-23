from datetime import date, datetime as dt

from zmanim_api.engine.shabbat import get_shabbat
from zmanim_api.engine.zmanim_module import get_zmanim
from zmanim_api.api_helpers import HavdalaChoices
from zmanim_api.models import ZmanimRequest
from ..consts import LAT, LNG, ZERO_ELEVATION, CL_OFFSET, PY_DATE


def test_regular_shabbat():
    expected = {
        'candle_lighting': dt.fromisoformat('2020-04-17T18:53:29.309197+03:00'),
        'havdala': dt.fromisoformat('2020-04-18T19:49:56.015490+03:00'),
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
    assert resp.model_dump(exclude_none=True, by_alias=True) == expected


def test_shabbat_with_late_cl_warning():
    expected = {
        'candle_lighting': dt.fromisoformat('2020-06-19T20:57:30.073986+03:00'),
        'havdala': dt.fromisoformat('2020-06-20T22:55:52.926784+03:00'),
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
    assert resp.model_dump(exclude_none=True, by_alias=True) == expected


def test_shabbat_with_tzeit_by_chatzot_layla():
    expected = {
        'candle_lighting': dt.fromisoformat('2021-07-30T22:49:19.853475+02:00'),
        'havdala': dt.fromisoformat('2021-08-01T00:22:38.590846+02:00'),
        'settings': {
            'date': date.fromisoformat('2021-07-24'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (69.77, 25.01),
            'elevation': 0
        },
        'torah_part': 'eikev',
        'late_cl_warning': True
    }

    resp = get_shabbat(69.77, 25.01, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees,
                       date(2021, 7, 24))
    assert resp.model_dump(exclude_none=True, by_alias=True) == expected


def test_shabbat_with_polar_daynight():
    expected = {
        'settings': {
            'date': date.fromisoformat('2021-07-25'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (76.60, 103.45),
            'elevation': 0
        },
        'torah_part': 'eikev',
        'late_cl_warning': True
    }

    resp = get_shabbat(76.60, 103.45, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees,
                       date(2021, 7, 25))
    assert resp.model_dump(exclude_none=True, by_alias=True) == expected


def test_shabbat_with_different_parsha():
    expected_1 = {
        'candle_lighting': dt.fromisoformat('2020-06-05T19:26:17.092514+03:00'),
        'havdala': dt.fromisoformat('2020-06-06T20:26:54.026459+03:00'),
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
        'candle_lighting': dt.fromisoformat('2020-06-05T19:41:17.010714+03:00'),
        'havdala': dt.fromisoformat('2020-06-06T20:46:30.467608+03:00'),
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

    assert resp_1.model_dump(exclude_none=True, by_alias=True) == expected_1
    assert resp_2.model_dump(exclude_none=True, by_alias=True) == expected_2


def test_shabbat_with_yomtov():
    expected_1 = {
        'candle_lighting': dt.fromisoformat('2020-05-29T19:22:26.312364+03:00'),
        'havdala': dt.fromisoformat('2020-05-30T20:22:41.756404+03:00'),
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
        'candle_lighting': dt.fromisoformat('2020-05-29T19:36:44.444321+03:00'),
        'havdala': dt.fromisoformat('2020-05-30T20:41:28.277038+03:00'),
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
        'candle_lighting': dt.fromisoformat('2020-04-10T18:53:49.571051+03:00'),
        'havdala': dt.fromisoformat('2020-04-11T19:52:51.908138+03:00'),
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

    assert resp_1.model_dump(exclude_none=True, by_alias=True) == expected_1
    assert resp_2.model_dump(exclude_none=True, by_alias=True) == expected_2
    assert resp_3.model_dump(exclude_none=True, by_alias=True) == expected_3


def test_shabbat_havdala_keeps_seconds():
    # clients round havdala up to the next whole minute, which only works
    # if the seconds survive — truncating here made havdala too early
    resp = get_shabbat(LAT, LNG, ZERO_ELEVATION, CL_OFFSET, HavdalaChoices.tzeis_8_5_degrees, PY_DATE)
    zmanim = get_zmanim(date(2020, 4, 18), LAT, LNG, ZERO_ELEVATION, ZmanimRequest())

    assert resp.havdala == zmanim.tzeis_8_5_degrees
    assert resp.havdala.second != 0
