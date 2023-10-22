from datetime import date, datetime as dt

from zmanim_api.engine.holidays import fast
from zmanim_api.api_helpers import FastsChoices
from ..consts import LAT, LNG, ZERO_ELEVATION, PY_DATE


def test_regular_fast():
    expected = {
        'settings': {
            'date': date.fromisoformat('2020-04-15'),
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': 'fast_9_av'
        },
        'moved_fast': False,
        'fast_start': dt.fromisoformat('2020-07-29T19:39:46.806374+03:00'),
        'chatzot': dt.fromisoformat('2020-07-30T12:46:47.783707+03:00'),
        'havdala_42_min': dt.fromisoformat('2020-07-30T20:21:01.912951+03:00'),
        'havdala_5_95_dgr': dt.fromisoformat('2020-07-30T20:05:29.105997+03:00'),
        'havdala_8_5_dgr': dt.fromisoformat('2020-07-30T20:18:58.749568+03:00')
    }

    actual = fast(
        FastsChoices.fast_9_av.value,
        PY_DATE,
        LAT,
        LNG,
        ZERO_ELEVATION
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_moved_fast_esther():
    expected = {
        'settings': {
            'date': date.fromisoformat('2024-01-15'),
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': 'fast_esther'
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2024-03-21T04:30:13.115829+02:00'),
        'havdala_42_min': dt.fromisoformat('2024-03-21T18:34:57.556976+02:00'),
        'havdala_5_95_dgr': dt.fromisoformat('2024-03-21T18:17:09.706478+02:00'),
        'havdala_8_5_dgr': dt.fromisoformat('2024-03-21T18:29:15.548910+02:00')
    }

    actual = fast(
        FastsChoices.fast_esther.value,
        date(2024, 1, 15),
        LAT,
        LNG,
        ZERO_ELEVATION
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_moved_fast_tammuz_and_av():
    expected_1 = {
        'settings': {
            'date': date.fromisoformat('2019-01-15'),
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': 'fast_17_tammuz'
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2019-07-21T04:23:50.558258+03:00'),
        'havdala_42_min': dt.fromisoformat('2019-07-21T20:27:20.849848+03:00'),
        'havdala_5_95_dgr': dt.fromisoformat('2019-07-21T20:12:23.808687+03:00'),
        'havdala_8_5_dgr': dt.fromisoformat('2019-07-21T20:26:14.766497+03:00')
    }
    expected_2 = {
        'settings': {
            'date': date.fromisoformat('2019-01-15'),
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': 'fast_9_av'
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2019-08-10T19:30:10.266510+03:00'),
        'chatzot': dt.fromisoformat('2019-08-11T12:45:36.210526+03:00'),
        'havdala_42_min': dt.fromisoformat('2019-08-11T20:11:11.913263+03:00'),
        'havdala_5_95_dgr': dt.fromisoformat('2019-08-11T19:54:56.938923+03:00'),
        'havdala_8_5_dgr': dt.fromisoformat('2019-08-11T20:08:01.465638+03:00')
    }

    actual_1 = fast(
        FastsChoices.fast_17_tammuz.value,
        date(2019, 1, 15),
        LAT,
        LNG,
        ZERO_ELEVATION
    )
    actual_2 = fast(
        FastsChoices.fast_9_av.value,
        date(2019, 1, 15),
        LAT,
        LNG,
        ZERO_ELEVATION,
    )

    assert actual_1.model_dump(exclude_none=True, by_alias=True) == expected_1
    assert actual_2.model_dump(exclude_none=True, by_alias=True) == expected_2


def test_day_after_moved_fast_tammuz_and_av():
    expected_1 = {
        'settings': {
            'date': date.fromisoformat('2022-07-17'),
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': 'fast_17_tammuz'
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2022-07-17T04:20:45.436601+03:00'),
        'havdala_42_min': dt.fromisoformat('2022-07-17T20:29:10.152776+03:00'),
        'havdala_5_95_dgr': dt.fromisoformat('2022-07-17T20:14:25.670857+03:00'),
        'havdala_8_5_dgr': dt.fromisoformat('2022-07-17T20:28:24.129112+03:00')
    }
    expected_2 = {
        'settings': {
            'date': date.fromisoformat('2022-08-07'),
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'fast_name': 'fast_9_av'
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2022-08-06T19:33:38.618130+03:00'),
        'chatzot': dt.fromisoformat('2022-08-07T12:46:08.569260+03:00'),
        'havdala_42_min': dt.fromisoformat('2022-08-07T20:14:44.393678+03:00'),
        'havdala_5_95_dgr': dt.fromisoformat('2022-08-07T19:58:43.183910+03:00'),
        'havdala_8_5_dgr': dt.fromisoformat('2022-08-07T20:11:55.916590+03:00')
    }
    actual_1 = fast(
        FastsChoices.fast_17_tammuz.value,
        date(2022, 7, 17),
        LAT,
        LNG,
        ZERO_ELEVATION
    )
    actual_2 = fast(
        FastsChoices.fast_9_av.value,
        date(2022, 8, 7),
        LAT,
        LNG,
        ZERO_ELEVATION,
    )

    assert actual_1.model_dump(exclude_none=True, by_alias=True) == expected_1
    assert actual_2.model_dump(exclude_none=True, by_alias=True) == expected_2


def test_9_of_av_in_north():
    expected = {
        'settings': {
            'date': date.fromisoformat('2021-07-24'),
            'coordinates': (63.44563381372263, 13.49966869597185),
            'elevation': 0,
            'fast_name': 'fast_17_tammuz'
        },
        'moved_fast': True,
        'fast_start': dt.fromisoformat('2022-07-17T01:11:01.899904+02:00'),
        'havdala_42_min': dt.fromisoformat('2022-07-17T23:29:10.694261+02:00')
    }

    actual = fast(
        FastsChoices.fast_17_tammuz.value,
        date(2021, 7, 24),
        63.44563381372263,
        13.49966869597185,
        ZERO_ELEVATION,
    ).model_dump(exclude_none=True, by_alias=True)
    assert actual == expected
