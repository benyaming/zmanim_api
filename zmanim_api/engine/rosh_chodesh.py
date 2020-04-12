from datetime import datetime as dt, date, timedelta

from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar


def get_next_rosh_chodesh(date_: date = None) -> dict:
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
    return rh_data




    # now = get_hebrew_now(date, rh_mode=True)
    #
    # month = Month(now.year, now.month)
    # month_dates = [day for day in month.iterdates()]
    #
    # if len(month_dates) == 29:
    #     rh_len = 1
    #     rh_heb_dates = [month_dates[-1] + 1]
    # else:
    #     rh_len = 2
    #     rh_heb_dates = [month_dates[-1], month_dates[-1] + 1]
    #
    # rh_dates = []
    # for day in rh_heb_dates:
    #     gr_day = day.to_pydate()
    #     date = {
    #         'day': gr_day.day,
    #         'month': gr_day.month,
    #         'year': gr_day.year,
    #         'weekday': gr_day.weekday()
    #     }
    #     rh_dates.append(date)
    #
    # rh_data = {
    #     'month_name': (month + 1).name,
    #     'days': rh_dates,
    #     'duration': rh_len,
    #     'molad': get_next_molad(now)
    # }
    # rh_data = {
    #
    # }
    #
    # return rh_data

# get_next_rosh_chodesh(Date(2020, 8, 23))
