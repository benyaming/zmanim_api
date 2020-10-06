from datetime import datetime as dt, date

import pytest

from test.consts import LAT, LNG
from zmanim_api.api_helpers import (
    validate_date_or_get_now,
    validate_datetime_or_get_now,
    DateException
)


def test_validate_date_or_get_now_without_args():
    resp = validate_date_or_get_now(None)
    assert isinstance(resp, date), True


def test_validate_date_or_get_now_with_correct_arg():
    expexted = date(2020, 4, 15)
    resp = validate_date_or_get_now('2020-04-15')
    assert resp == expexted


def test_validate_date_or_get_now_with_incorrect_arg():
    with pytest.raises(DateException):
        validate_date_or_get_now('15/04/2020')


def test_validate_datetime_or_get_now_without_args():
    resp = validate_datetime_or_get_now(None, LAT, LNG)
    assert isinstance(resp, dt), True


def test_validate_datetime_or_get_now_with_correct_arg():
    expexted = dt(2020, 4, 15, 16, 55)
    resp = validate_datetime_or_get_now('2020-04-15T16:55', LAT, LNG)
    assert resp == expexted


def test_validate_datetime_or_get_now_with_incorrect_arg():
    with pytest.raises(DateException):
        validate_datetime_or_get_now('15/04/2020 16:55', LAT, LNG)
