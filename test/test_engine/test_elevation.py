from datetime import date, timedelta

from zmanim_api.engine.holidays import fast
from zmanim_api.engine.zmanim_module import get_zmanim
from zmanim_api.api_helpers import FastsChoices
from zmanim_api.models import ZmanimRequest
from ..consts import LAT, LNG, ZERO_ELEVATION

ELEVATION = 150
FAST_DATE = date(2026, 7, 5)
ZMANIM_DATE = date(2026, 7, 23)  # 9 av 5786


def test_fast_havdala_42_matches_zmanim_tzeis_42():
    fast_data = fast(FastsChoices.fast_9_av.value, FAST_DATE, LAT, LNG, ELEVATION)
    zmanim = get_zmanim(ZMANIM_DATE, LAT, LNG, ELEVATION, ZmanimRequest())

    assert fast_data.havdala_42_min == zmanim.tzeis_42_minutes
    assert fast_data.havdala_42_min == zmanim.sunset + timedelta(minutes=42)


def test_elevation_shifts_offset_based_zmanim():
    at_sea_level = get_zmanim(ZMANIM_DATE, LAT, LNG, ZERO_ELEVATION, ZmanimRequest())
    at_elevation = get_zmanim(ZMANIM_DATE, LAT, LNG, ELEVATION, ZmanimRequest())

    assert at_elevation.sunrise < at_sea_level.sunrise
    assert at_elevation.sunset > at_sea_level.sunset
    assert at_elevation.tzeis_42_minutes > at_sea_level.tzeis_42_minutes
    assert at_elevation.tzeis_72_minutes > at_sea_level.tzeis_72_minutes
    assert at_elevation.astronomical_hour_gra > at_sea_level.astronomical_hour_gra


def test_elevation_does_not_affect_degree_based_zmanim():
    at_sea_level = get_zmanim(ZMANIM_DATE, LAT, LNG, ZERO_ELEVATION, ZmanimRequest())
    at_elevation = get_zmanim(ZMANIM_DATE, LAT, LNG, ELEVATION, ZmanimRequest())

    assert at_elevation.tzeis_5_95_degrees == at_sea_level.tzeis_5_95_degrees
    assert at_elevation.tzeis_8_5_degrees == at_sea_level.tzeis_8_5_degrees
    assert at_elevation.alos == at_sea_level.alos
    assert at_elevation.misheyakir_10_2 == at_sea_level.misheyakir_10_2
    assert at_elevation.chatzos == at_sea_level.chatzos


def test_elevation_shifts_fast_start():
    at_sea_level = fast(FastsChoices.fast_9_av.value, FAST_DATE, LAT, LNG, ZERO_ELEVATION)
    at_elevation = fast(FastsChoices.fast_9_av.value, FAST_DATE, LAT, LNG, ELEVATION)

    # 9 av fast starts at shkia, which follows elevation
    assert at_elevation.fast_start > at_sea_level.fast_start
    # degree-based havdala stays sea-level
    assert at_elevation.havdala_8_5_dgr == at_sea_level.havdala_8_5_dgr
    assert at_elevation.havdala_5_95_dgr == at_sea_level.havdala_5_95_dgr
