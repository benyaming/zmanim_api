from datetime import date

from zmanim_api.utils import get_next_weekday


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
