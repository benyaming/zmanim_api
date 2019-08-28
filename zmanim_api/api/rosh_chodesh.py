import sqlite3
from datetime import datetime as dt

from pyluach.hebrewcal import HebrewDate, Month

from zmanim_api.api.utils import get_hebrew_now


def get_molad_from_db(year: int, month: int) -> tuple:
    with sqlite3.connect('molad.db') as conn:  # type: sqlite3.Connection
        cur = conn.cursor()
        query = 'SELECT molad_day, molad_month, molad_weekday, molad_hours, ' \
                'molad_minutes, molad_parts ' \
                'FROM molad ' \
                'WHERE year = ? AND month = ?'
        molad = cur.execute(query, (year, month)).fetchone()
        return molad


def get_next_molad() -> dict:
    now = get_hebrew_now()
    year, month = now.year, now.month
    # we looking for next month's molad and not for tishrei
    month += 1 if month != 7 else 2
    molad_data = get_molad_from_db(year, month)

    molad = {
        'molad_day': molad_data[0],
        'molad_month': molad_data[1],
        'molad_weekday': molad_data[2],
        'molad_hour': molad_data[3],
        'molad_minutes': molad_data[4],
        'molad_parts': molad_data[5],
    }
    return molad


def get_next_rosh_chodesh(date: str) -> dict:
    # todo custom date
    now = get_hebrew_now()
    # if rosh chodesh today, move to previous day
    if now.day == 30 or now.day == 1:
        now -= 1

    month = Month(now.year, now.month)
    month_dates = [day for day in month.iterdates()]

    if len(month_dates) == 29:
        rh_len = 1
        rh_heb_dates = [month_dates[-1] + 1]
    else:
        rh_len = 2
        rh_heb_dates = [month_dates[-1], month_dates[-1] + 1]

    rh_dates = []
    for day in rh_heb_dates:
        gr_day = day.to_pydate()
        date = {
            'day': gr_day.day,
            'month': gr_day.month,
            'year': gr_day.year,
            'weekday': gr_day.weekday()
        }
        rh_dates.append(date)

    rh_data = {
        'days': rh_dates,
        'duration': rh_len,
        'molad': get_next_molad()
    }

    return rh_data
