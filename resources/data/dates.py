from datetime import datetime, timedelta

from pytz import all_timezones, timezone


def get_dates():

  class Dates:
    arg_tz = list(filter(lambda x: 'Buenos_Aires' in x, all_timezones)).pop(0)
    ARG = timezone(arg_tz)
    current_date = datetime.now(tz=ARG)
    previous_date = current_date - timedelta(days=1)
    current_year = current_date.year
    previous_year = current_year - 1
    current_month = current_date.month
    previous_month = current_month - 1 if current_month != 1 else 12
    current_day = current_date.day
    previous_day = previous_date.day

  return Dates
