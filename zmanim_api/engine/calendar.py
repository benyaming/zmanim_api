from zmanim.zmanim_calendar import ZmanimCalendar as _ZmanimCalendar


class ZmanimCalendar(_ZmanimCalendar):
    # Elevation must affect offset-based zmanim (shkia, hanetz, tzeis by
    # minutes, shaos zmaniyos); degree-based zmanim and candle lighting
    # stay sea-level as usual.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_elevation = True
