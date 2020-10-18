import pytest
from fastapi.testclient import TestClient

from zmanim_api.main import app
from ..consts import GEO_DATE_PARAMS, ASUR_BEMELACHA_PARAMS, DATE, HAVDALA


client = TestClient(app)


@pytest.mark.api
@pytest.mark.zmanim
def test_zmanim_endpoint():
    params = GEO_DATE_PARAMS
    json = {
        'sunrise': True,
        'alos': True,
        'sof_zman_tefila_gra': True,
        'sof_zman_tefila_ma': True,
        'misheyakir_10_2': True,
        'sof_zman_shema_gra': True,
        'sof_zman_shema_ma': True,
        'chatzos': True,
        'mincha_ketana': True,
        'mincha_gedola': True,
        'plag_mincha': True,
        'sunset': True,
        'tzeis_8_5_degrees': True,
        'tzeis_72_minutes': True,
        'tzeis_42_minutes': True,
        'tzeis_5_95_degrees': True,
        'chatzot_laila': True,
        'astronomical_hour_ma': True,
        'astronomical_hour_gra': True
    }

    expected = {
        'settings': {
            'date': '2020-04-15',
            'jewish_date': '5780-1-21',
            'coordinates': [
                32.09,
                34.86
            ],
            'elevation': 0
        },
        'sunrise': '2020-04-15T06:11:24.317714+03:00',
        'alos': '2020-04-15T04:55:46.643596+03:00',
        'sof_zman_tefila_gra': '2020-04-15T10:30:58.115338+03:00',
        'sof_zman_tefila_ma': '2020-04-15T10:06:58.115338+03:00',
        'misheyakir_10_2': '2020-04-15T05:25:33.360431+03:00',
        'sof_zman_shema_gra': '2020-04-15T09:26:04.665932+03:00',
        'mincha_ketana': '2020-04-15T16:27:52.087071+03:00',
        'sof_zman_shema_ma': '2020-04-15T08:50:04.665932+03:00',
        'chatzos': '2020-04-15T12:40:45.014150+03:00',
        'mincha_gedola': '2020-04-15T13:13:11.738853+03:00',
        'plag_mincha': '2020-04-15T17:48:58.898828+03:00',
        'sunset': '2020-04-15T19:10:05.710586+03:00',
        'tzeis_8_5_degrees': '2020-04-15T19:47:36.366258+03:00',
        'tzeis_72_minutes': '2020-04-15T20:22:05.710586+03:00',
        'tzeis_42_minutes': '2020-04-15T19:52:05.710586+03:00',
        'tzeis_5_95_degrees': '2020-04-15T19:35:01.557256+03:00',
        'astronomical_hour_ma': '01:16:53',
        'astronomical_hour_gra': '01:04:53'
    }

    resp = client.post('/zmanim', params=params, json=json)

    assert resp.status_code == 200
    assert resp.json() == expected


@pytest.mark.api
@pytest.mark.shabbat
def test_shabbat_endpoint():
    params = {**GEO_DATE_PARAMS, **ASUR_BEMELACHA_PARAMS}
    expected = {
        'candle_lighting': '2020-04-17T18:53:00+03:00',
        'havdala': '2020-04-18T19:49:00+03:00',
        'settings': {
            'date': '2020-04-15',
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': [
                32.09,
                34.86
            ],
            'elevation': 0
        },
        'torah_part': 'shemini',
        'late_cl_warning': False
    }

    resp = client.get('/shabbat', params=params)
    assert resp.json() == expected


@pytest.mark.api
@pytest.mark.rosh_chodesh
def test_rosh_chodesh_endpoint():
    params = {'date': DATE}
    expected = {
        'settings': {
            'date': '2020-04-15'
        },
        'month_name': 'iyar',
        'days': [
            '2020-04-24',
            '2020-04-25'
        ],
        'duration': 2,
        'molad': [
            '2020-04-22T22:58',
            12
        ]
    }

    resp = client.get('/rosh_chodesh', params=params)
    assert resp.json() == expected


@pytest.mark.api
@pytest.mark.daf_yomi
def test_daf_yomi_endpoint():
    params = {'date': GEO_DATE_PARAMS['date']}
    expected = {
        'settings': {
            'date': '2020-04-15'
        },
        'masehet': "shabbos",
        'daf': 40
    }

    resp = client.get('/daf_yomi', params=params)
    assert resp.json() == expected


@pytest.mark.api
@pytest.mark.holiday
def test_holiday_endpoint():
    params = {
        'holiday_name': 'purim',
        'date': DATE
    }
    expected = {
        "settings": {
            "date": "2020-04-15",
            "holiday_name": "purim"
        },
        "date": "2021-02-26"
    }

    resp = client.get('/holiday', params=params)
    assert resp.json() == expected


@pytest.mark.api
@pytest.mark.yomtov
def test_yomtov_endpoint():
    params = {
        **GEO_DATE_PARAMS,
        **ASUR_BEMELACHA_PARAMS,
        'yomtov_name': 'rosh_hashana'
    }
    expected = {
        'settings': {
            'date': '2020-04-15',
            'cl_offset': 18,
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': [
                32.09,
                34.86
            ],
            'elevation': 0,
            'yomtov_name': 'rosh_hashana'
        },
        'day_1': {
            'date': '2020-09-19',
            'candle_lighting': '2020-09-18T18:24:14.730847+03:00'
        },
        'day_2': {
            'date': '2020-09-20',
            'candle_lighting': '2020-09-19T19:17:11.477017+03:00',
            'havdala': '2020-09-20T19:15:50.475811+03:00'
        }
    }

    resp = client.get('/yom_tov', params=params)
    assert resp.json() == expected


@pytest.mark.api
@pytest.mark.fast
def test_fast_endpoint():
    params = {
        **GEO_DATE_PARAMS,
        'havdala': HAVDALA,
        'fast_name': 'fast_gedalia'
    }
    expected = {
        'settings': {
            'date': '2020-04-15',
            'havdala_opinion': 'tzeis_8_5_degrees',
            'coordinates': [
                32.09,
                34.86
            ],
            'elevation': 0,
            'fast_name': 'fast_gedalia'
        },
        'moved_fast': False,
        'fast_start': '2020-09-21T05:15:41.082623+03:00',
        'havdala': '2020-09-21T19:14:29.657488+03:00'
    }

    resp = client.get('/fast', params=params)
    assert resp.json() == expected


@pytest.mark.api
def test_asur_bemelacha_endpoint():
    params_1 = {
        'lat': GEO_DATE_PARAMS['lat'],
        'lng': GEO_DATE_PARAMS['lng'],
        'elevation': GEO_DATE_PARAMS['elevation'],
        'dt': '2020-09-27T12:00'
    }
    params_2 = {
        'lat': GEO_DATE_PARAMS['lat'],
        'lng': GEO_DATE_PARAMS['lng'],
        'elevation': GEO_DATE_PARAMS['elevation'],
        'dt': '2020-09-26T12:00'
    }
    expected_1 = {'result': False}
    expected_2 = {'result': True}

    actual_1 = client.get('/is_asur_bemelacha', params=params_1)
    actual_2 = client.get('/is_asur_bemelacha', params=params_2)
    assert actual_1.json() == expected_1
    assert actual_2.json() == expected_2
