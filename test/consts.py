from datetime import date


LAT = 32.09
LNG = 34.86
ZERO_ELEVATION = 0
DATE = '2020-04-15'
PY_DATE = date(2020, 4, 15)


GEO_DATE_PARAMS = {
    'date': DATE,
    'elevation': ZERO_ELEVATION,
    'lat': LAT,
    'lng': LNG
}

CL_OFFSET = 18
HAVDALA = 'tzeis_8_5_degrees'

ASUR_BEMELACHA_PARAMS = {
    'cl_offset': CL_OFFSET,
    'havdala': HAVDALA
}
