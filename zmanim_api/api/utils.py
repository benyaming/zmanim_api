from timezonefinder import TimezoneFinder


def get_tz(lat: float, lng: float) -> str:
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=lng, lat=lat)
    return tz
