from pyluach.hebrewcal import HebrewDate, Year

for year in range(5700, 5800):
    month = 1
    date = HebrewDate(year, month, 15)
    if date.weekday() == 1:
        print(date)
