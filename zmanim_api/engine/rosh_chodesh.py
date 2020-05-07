from datetime import datetime as dt, date, timedelta

from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar

from ..models import RoshChodesh, SimpleSettings


def get_next_rosh_chodesh(date_: date = None) -> RoshChodesh:
    calendar = JewishCalendar(date_ or dt.now())

    if calendar.is_rosh_chodesh():
        return get_next_rosh_chodesh(date_ + timedelta(days=-1))

    if calendar.jewish_month == 6:
        return get_next_rosh_chodesh(date_ + timedelta(days=calendar.days_in_jewish_month()))

    month_length = calendar.days_in_jewish_month()
    days_until_rh = 30 - calendar.jewish_day
    calendar.forward(days_until_rh)

    rh_dates = [calendar.gregorian_date.isoformat()]
    if month_length == 30:
        rh_dates.append(calendar.forward().gregorian_date.isoformat())

    molad = calendar.molad()
    molad_iso = dt(molad.gregorian_year, molad.gregorian_month, molad.gregorian_day,
                   molad.molad_hours, molad.molad_minutes)

    rh_data = {
        'month_name': calendar.jewish_month_name(),
        'days': rh_dates,
        'duration': 1 if month_length == 29 else 2,
        'molad': [molad_iso, molad.molad_chalakim]
    }
    settings = SimpleSettings(date=date_ or dt.now())
    return RoshChodesh(settings=settings, **rh_data)

