from datetime import date, datetime as dt

from zmanim_api.engine.holidays import get_yom_tov
from zmanim_api.api_helpers import YomTovChoices, HavdalaChoices
from ..consts import LAT, LNG, ZERO_ELEVATION


def test_regular_yomtov_in_istael():
    expected = {
        'settings': {
            'date': date.fromisoformat('2021-04-15'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'yomtov_name': 'shavuot'
        },
        'day_1': {
            'date': date.fromisoformat('2021-05-17'),
            'candle_lighting': dt.fromisoformat('2021-05-16T19:13:51.154895+03:00'),
            'havdala': dt.fromisoformat('2021-05-17T20:13:02.790384+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.shavuot.value,
        date(2021, 4, 15),
        LAT,
        LNG,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_regular_yomtov_in_diaspora():
    expected = {
        'settings': {
            'date': date.fromisoformat('2021-04-15'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (55.5, 37.7),
            'elevation': 0,
            'yomtov_name': 'shavuot'
        },
        'day_1': {
            'date': date.fromisoformat('2021-05-17'),
            'candle_lighting': dt.fromisoformat('2021-05-16T20:17:11.838274+03:00')
        },
        'day_2': {
            'date': date.fromisoformat('2021-05-18'),
            'candle_lighting': dt.fromisoformat('2021-05-17T21:55:12.282469+03:00'),
            'havdala': dt.fromisoformat('2021-05-18T21:57:45.263860+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.shavuot.value,
        date(2021, 4, 15),
        55.5,
        37.7,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_past_yomtov():
    expected = {
        'settings': {
            'date': date.fromisoformat('2019-04-01'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'yomtov_name': 'succot'
        },
        'day_1': {
            'date': date.fromisoformat('2019-10-14'),
            'candle_lighting': dt.fromisoformat('2019-10-13T17:53:03.590573+03:00'),
            'havdala': dt.fromisoformat('2019-10-14T18:46:18.069214+03:00')
        },
        'hoshana_rabba': date.fromisoformat('2019-10-20')
    }

    actual = get_yom_tov(
        YomTovChoices.succot.value,
        date(2019, 4, 1),
        LAT,
        LNG,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_rosh_hashana_in_diaspora():
    expected = {
        'settings': {
            'date': date.fromisoformat('2021-04-15'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (55.5, 37.7),
            'elevation': 0,
            'yomtov_name': 'rosh_hashana'
        },
        'day_1': {
            'date': date.fromisoformat('2021-09-07'),
            'candle_lighting': dt.fromisoformat('2021-09-06T18:51:44.012224+03:00')
        },
        'day_2': {
            'date': date.fromisoformat('2021-09-08'),
            'candle_lighting': dt.fromisoformat('2021-09-07T20:03:54.173229+03:00'),
            'havdala': dt.fromisoformat('2021-09-08T20:01:06.268724+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.rosh_hashana.value,
        date(2021, 4, 15),
        55.5,
        37.7,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_pre_shabbat_in_israel():
    expected = {
        'settings': {
            'date': date.fromisoformat('2022-04-01'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'yomtov_name': 'shavuot'
        },
        'pre_shabbat': {
            'date': date.fromisoformat('2022-06-04'),
            'candle_lighting': dt.fromisoformat('2022-06-03T19:25:00.047838+03:00')
        },
        'day_1': {
            'date': date.fromisoformat('2022-06-05'),
            'candle_lighting': dt.fromisoformat('2022-06-04T20:25:30.621846+03:00'),
            'havdala': dt.fromisoformat('2022-06-05T20:26:05.207323+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.shavuot.value,
        date(2022, 4, 1),
        LAT,
        LNG,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_pre_shabbat_in_diaspora():
    expected = {
        'settings': {
            'date': date.fromisoformat('2022-04-01'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (55.5, 37.7),
            'elevation': 0,
            'yomtov_name': 'shavuot'
        },
        'pre_shabbat': {
            'date': date.fromisoformat('2022-06-04'),
            'candle_lighting': dt.fromisoformat('2022-06-03T20:44:39.375578+03:00')
        },
        'day_1': {
            'date': date.fromisoformat('2022-06-05'),
            'candle_lighting': dt.fromisoformat('2022-06-04T22:36:39.212694+03:00'),
        },
        'day_2': {
            'date': date.fromisoformat('2022-06-06'),
            'candle_lighting': dt.fromisoformat('2022-06-05T22:38:33.390085+03:00'),
            'havdala': dt.fromisoformat('2022-06-06T22:40:23.180390+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.shavuot.value,
        date(2022, 4, 1),
        55.5,
        37.7,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_post_shabbat_in_israel():
    expected = {
        'settings': {
            'date': date.fromisoformat('2020-04-15'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.09, 34.86),
            'elevation': 0,
            'yomtov_name': 'shavuot'
        },
        'day_1': {
            'date': date.fromisoformat('2020-05-29'),
            'candle_lighting': dt.fromisoformat('2020-05-28T19:21:50.464019+03:00')
        },
        'post_shabbat': {
            'date': date.fromisoformat('2020-05-30'),
            'candle_lighting': dt.fromisoformat('2020-05-29T19:22:26.312364+03:00'),
            'havdala': dt.fromisoformat('2020-05-30T20:22:41.756404+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.shavuot.value,
        date(2020, 4, 15),
        LAT,
        LNG,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_post_shabbat_in_diaspora():
    expected = {
        'settings': {
            'date': date.fromisoformat('2020-04-01'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (55.5, 37.7),
            'elevation': 0,
            'yomtov_name': 'pesach'
        },
        'pesach_burning_chanetz_till': dt.fromisoformat('2020-04-08T11:23:16:659939+03:00'),
        'pesach_eating_chanetz_till': dt.fromisoformat('2020-04-08T10:14:58:519048+03:00'),
        'day_1': {
            'date': date.fromisoformat('2020-04-09'),
            'candle_lighting': dt.fromisoformat('2020-04-08T19:03:23.646179+03:00')
        },
        'day_2': {
            'date': date.fromisoformat('2020-04-10'),
            'candle_lighting': dt.fromisoformat('2020-04-09T20:21:45.269644+03:00')
        },
        'post_shabbat': {
            'date': date.fromisoformat('2020-04-11'),
            'candle_lighting': dt.fromisoformat('2020-04-10T19:07:23.016963+03:00'),
            'havdala': dt.fromisoformat('2020-04-11T20:26:20.026278+03:00')
        },
        'pesach_part_2_day_1': {
            'date': date.fromisoformat('2020-04-15'),
            'candle_lighting': dt.fromisoformat('2020-04-14T19:15:22.104678+03:00')
        },
        'pesach_part_2_day_2': {
            'date': date.fromisoformat('2020-04-16'),
            'candle_lighting': dt.fromisoformat('2020-04-15T20:35:38.135050+03:00'),
            'havdala': dt.fromisoformat('2020-04-16T20:37:59.486154+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.pesach.value,
        date(2020, 4, 1),
        55.5,
        37.7,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_second_yt_is_shabbat():
    expected = {
        'settings': {
            'date': date.fromisoformat('2021-07-24'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (55.63097, 37.628591),
            'elevation': 0,
            'yomtov_name': 'pesach'
        },
        'pesach_burning_chanetz_till': dt.fromisoformat('2022-04-15T11:19:24:184815+03:00'),
        'pesach_eating_chanetz_till': dt.fromisoformat('2022-04-15T10:08:36:127354+03:00'),
        'day_1': {
            'date': date.fromisoformat('2022-04-16'),
            'candle_lighting': dt.fromisoformat('2022-04-15T19:17:00.587041+03:00')
        },
        'day_2': {
            'date': date.fromisoformat('2022-04-17'),
            'candle_lighting': dt.fromisoformat('2022-04-16T20:37:44.000668+03:00'),
            'havdala': dt.fromisoformat('2022-04-17T20:40:06.767369+03:00')
        },
        'pesach_part_2_day_1': {
            'date': date.fromisoformat('2022-04-22'),
            'candle_lighting': dt.fromisoformat('2022-04-21T19:29:03.967858+03:00')
        },
        'pesach_part_2_day_2': {
            'date': date.fromisoformat('2022-04-23'),
            'candle_lighting': dt.fromisoformat('2022-04-22T19:31:04.444159+03:00'),
            'havdala': dt.fromisoformat('2022-04-23T20:54:39.137197+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.pesach.value,
        date(2021, 7, 24),
        55.63097,
        37.628591,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected


def test_peesach_part_2_post_shabbat_in_istael():
    expected = {
        'settings': {
            'date': date.fromisoformat('2022-04-12'),
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': (32.08335, 34.883325),
            'elevation': 0,
            "yomtov_name": "pesach"
        },
        'pesach_burning_chanetz_till': dt.fromisoformat('2022-04-15T11:35:57:473214+03:00'),
        'pesach_eating_chanetz_till': dt.fromisoformat('2022-04-15T10:31:08:593221+03:00'),
        'day_1': {
            "date": date.fromisoformat('2022-04-16'),
            "candle_lighting": dt.fromisoformat('2022-04-15T18:51:39.633162+03:00'),
            "havdala": dt.fromisoformat('2022-04-16T19:47:54.176159+03:00')
        },
        'pesach_part_2_day_1': {
            "date": date.fromisoformat('2022-04-22'),
            "candle_lighting": dt.fromisoformat('2022-04-21T18:55:51.226349+03:00')
        },
        'pesach_part_2_post_shabat': {
            'date': date.fromisoformat('2022-04-23'),
            'candle_lighting': dt.fromisoformat('2022-04-22T18:56:33.479101+03:00'),
            'havdala': dt.fromisoformat('2022-04-23T19:53:23.397083+03:00')
        }
    }

    actual = get_yom_tov(
        YomTovChoices.pesach.value,
        date(2022, 4, 12),
        32.08335,
        34.883325,
        ZERO_ELEVATION,
        18,
        HavdalaChoices.tzeis_8_5_degrees
    )
    assert actual.model_dump(exclude_none=True, by_alias=True) == expected
