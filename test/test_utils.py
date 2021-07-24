from datetime import date

from zmanim_api.utils import get_next_weekday, get_tz


def test_get_next_weekday():
    weekday = 5
    d1 = date(2020, 9, 22)
    d2 = date(2020, 9, 25)
    d3 = date(2020, 9, 26)
    d4 = date(2020, 9, 27)

    expected_1 = date(2020, 9, 22)
    expected_2 = date(2020, 10, 3)

    assert get_next_weekday(d1, weekday), expected_1
    assert get_next_weekday(d2, weekday), expected_1
    assert get_next_weekday(d3, weekday), expected_2
    assert get_next_weekday(d4, weekday), expected_2


def test_get_tz():
    loc1 = 55.5, 37.7
    loc2 = 32.09, 34.87
    loc3 = 31.54, 35.25
    loc4 = 40.68, -73.96

    expected_1 = 'Europe/Moscow'
    expected_2 = 'Asia/Jerusalem'
    expected_3 = 'Asia/Jerusalem'
    expected_4 = 'America/New_York'

    assert get_tz(*loc1), expected_1
    assert get_tz(*loc2), expected_2
    assert get_tz(*loc3), expected_3
    assert get_tz(*loc4), expected_4
