from datetime import date, datetime as dt

import pytest

from zmanim_api.engine.holidays import fast
from zmanim_api.api_helpers import FastsChoises, HavdalaChoises
from ..consts import LAT, LNG, ZERO_ELEVATION, PY_DATE


def test_regular_fast():
    expected = {
        'settings': {
            'date': date.fromisoformat('2020-04-15'),
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': "fast_9_av"
        },
        'moved_fast': False,
        'fast_start': dt.fromisoformat('2020-07-29T19:39:46.806374+03:00'),
        'chatzot': dt.fromisoformat('2020-07-30T12:46:47.783707+03:00'),
        'havdala': dt.fromisoformat('2020-07-30T20:18:58.749568+03:00')
    }

    actual = fast(
        FastsChoises.fast_9_av.value,
        PY_DATE,
        LAT,
        LNG,
        ZERO_ELEVATION,
        HavdalaChoises.tzeis_8_5_degrees
    )
    assert actual.dict(exclude_none=True, by_alias=True) == expected


def test_moved_fast_esther():
    expected = {
        'settings': {
            'date': date.fromisoformat('2024-01-15'),
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': "fast_esther"
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2024-03-21T04:30:13.115829+02:00'),
        'havdala': dt.fromisoformat('2024-03-21T18:29:15.548910+02:00')
    }

    actual = fast(
        FastsChoises.fast_esther.value,
        date(2024, 1, 15),
        LAT,
        LNG,
        ZERO_ELEVATION,
        HavdalaChoises.tzeis_8_5_degrees
    )
    assert actual.dict(exclude_none=True, by_alias=True) == expected


def test_moved_fast_tammuz_and_av():
    expected_1 = {
        'settings': {
            'date': date.fromisoformat('2019-01-15'),
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': "fast_17_tammuz"
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2019-07-21T04:23:50.558258+03:00'),
        'havdala': dt.fromisoformat('2019-07-21T20:26:14.766497+03:00')
    }
    expected_2 = {
        'settings': {
            'date': date.fromisoformat('2019-01-15'),
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': "fast_9_av"
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2019-08-10T19:30:10.266510+03:00'),
        'chatzot': dt.fromisoformat('2019-08-11T12:45:36.210526+03:00'),
        'havdala': dt.fromisoformat('2019-08-11T20:08:01.465638+03:00')
    }

    actual_1 = fast(
        FastsChoises.fast_17_tammuz.value,
        date(2019, 1, 15),
        LAT,
        LNG,
        ZERO_ELEVATION,
        HavdalaChoises.tzeis_8_5_degrees
    )
    actual_2 = fast(
        FastsChoises.fast_9_av.value,
        date(2019, 1, 15),
        LAT,
        LNG,
        ZERO_ELEVATION,
        HavdalaChoises.tzeis_8_5_degrees
    )

    assert actual_1.dict(exclude_none=True, by_alias=True) == expected_1
    assert actual_2.dict(exclude_none=True, by_alias=True) == expected_2


