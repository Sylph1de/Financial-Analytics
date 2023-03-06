from datetime import datetime, timedelta

from pytz import timezone


def get_dates():
  tz = timezone('America/Buenos_Aires')

  class Dates:

    current_date = datetime.now(tz)
    previous_date = current_date - timedelta(days=1)
    current_year = current_date.year
    previous_year = current_year - 1
    current_month = current_date.month
    previous_month = (current_date - timedelta(months=1)).month
    current_day = current_date.day
    previous_day = previous_date.day

  return Dates
