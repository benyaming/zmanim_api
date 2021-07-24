from datetime import date

from zmanim_api.engine.holidays import get_simple_holiday
from zmanim_api.api_helpers import SimpleHolidayChoices
from ..consts import PY_DATE


def test_regular_holiday():
    expected = {
        'settings': {
            'date': date.fromisoformat('2020-04-15'),
            'holiday_name': 'tu_bi_shvat'
        },
        'date': date.fromisoformat('2021-01-28')
    }

    actual = get_simple_holiday(SimpleHolidayChoices.tu_bi_shvat.value, PY_DATE)
    assert actual.dict(exclude_none=True, by_alias=True) == expected


def test_yom_hashoah():
    expected = {
        'settings': {
            'date': date.fromisoformat('2020-04-15'),
            'holiday_name': 'yom_hashoah'
        },
        'date': date.fromisoformat('2020-04-21')
    }

    actual = get_simple_holiday(SimpleHolidayChoices.yom_hashoah.value, PY_DATE)
    assert actual.dict(exclude_none=True, by_alias=True) == expected


def test_yom_hashoah_on_friday():
    expected = {
        'settings': {
            'date': date.fromisoformat('2021-04-01'),
            'holiday_name': 'yom_hashoah'
        },
        'date': date.fromisoformat('2021-04-08')
    }

    actual = get_simple_holiday(SimpleHolidayChoices.yom_hashoah.value, date(2021, 4, 1))
    assert actual.dict(exclude_none=True, by_alias=True) == expected


def test_yom_hashoah_on_sunday():
    expected = {
        'settings': {
            'date': date.fromisoformat('2024-04-01'),
            'holiday_name': 'yom_hashoah'
        },
        'date': date.fromisoformat('2024-05-06')
    }

    actual = get_simple_holiday(SimpleHolidayChoices.yom_hashoah.value, date(2024, 4, 1))
    assert actual.dict(exclude_none=True, by_alias=True) == expected


def test_yom_hazikaron():
    expected = {
        'settings': {
            'date': date.fromisoformat('2020-04-15'),
            'holiday_name': 'yom_hazikaron'
        },
        'date': date.fromisoformat('2020-04-28')
    }

    actual = get_simple_holiday(SimpleHolidayChoices.yom_hazikaron.value, PY_DATE)
    assert actual.dict(exclude_none=True, by_alias=True) == expected


def test_yom_hazikaron_friday_yom_haatzmaut_shabbat():
    expected_1 = {
        'settings': {
            'date': date.fromisoformat('2021-04-01'),
            'holiday_name': 'yom_hazikaron'
        },
        'date': date.fromisoformat('2021-04-14')
    }
    expected_2 = {
        'settings': {
            'date': date.fromisoformat('2021-04-01'),
            'holiday_name': 'yom_haatzmaut'
        },
        'date': date.fromisoformat('2021-04-15')
    }

    actual_1 = get_simple_holiday(SimpleHolidayChoices.yom_hazikaron.value, date(2021, 4, 1))
    actual_2 = get_simple_holiday(SimpleHolidayChoices.yom_haatzmaut.value, date(2021, 4, 1))
    assert actual_1.dict(exclude_none=True, by_alias=True) == expected_1
    assert actual_2.dict(exclude_none=True, by_alias=True) == expected_2


def test_yom_hazikaron_shabbat_yom_haatzmaut_sunday():
    expected_1 = {
        'settings': {
            'date': date.fromisoformat('2024-04-01'),
            'holiday_name': 'yom_hazikaron'
        },
        'date': date.fromisoformat('2024-05-13')
    }
    expected_2 = {
        'settings': {
            'date': date.fromisoformat('2024-04-01'),
            'holiday_name': 'yom_haatzmaut'
        },
        'date': date.fromisoformat('2024-05-14')
    }

    actual_1 = get_simple_holiday(SimpleHolidayChoices.yom_hazikaron.value, date(2024, 4, 1))
    actual_2 = get_simple_holiday(SimpleHolidayChoices.yom_haatzmaut.value, date(2024, 4, 1))
    assert actual_1.dict(exclude_none=True, by_alias=True) == expected_1
    assert actual_2.dict(exclude_none=True, by_alias=True) == expected_2


def test_yom_hazikaron_wednesdey_yom_haatzmaut_thursday():
    expected_1 = {
        'settings': {
            'date': date.fromisoformat('2022-04-01'),
            'holiday_name': 'yom_hazikaron'
        },
        'date': date.fromisoformat('2022-05-04')
    }
    expected_2 = {
        'settings': {
            'date': date.fromisoformat('2022-04-01'),
            'holiday_name': 'yom_haatzmaut'
        },
        'date': date.fromisoformat('2022-05-05')
    }

    actual_1 = get_simple_holiday(SimpleHolidayChoices.yom_hazikaron.value, date(2022, 4, 1))
    actual_2 = get_simple_holiday(SimpleHolidayChoices.yom_haatzmaut.value, date(2022, 4, 1))
    assert actual_1.dict(exclude_none=True, by_alias=True) == expected_1
    assert actual_2.dict(exclude_none=True, by_alias=True) == expected_2


def test_holiday_ducing_holiday():
    expected = {
        'settings': {
            'date': date.fromisoformat('2021-12-01'),
            'holiday_name': 'chanukah'
        },
        'date': date.fromisoformat('2021-11-29')
    }

    actual = get_simple_holiday(SimpleHolidayChoices.chanukah.value, date(2021, 12, 1)).dict(exclude_none=True, by_alias=True)
    assert actual == expected
