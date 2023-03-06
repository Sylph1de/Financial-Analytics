from resources.data.dates import get_dates


def get_masks(df):
  Dates = get_dates()

  class Masks:
    # # ? Yearly masks
    # previous_yearly_mask = df.Fecha.dt.year == Dates.previous_year
    # current_yearly_mask = df.Fecha.dt.year == Dates.current_year

    # # ? Monthly masks
    # previous_monthly_mask = (df.Fecha.dt.year == Dates.current_year) & (df.Fecha.dt.month == Dates.previous_month)
    # current_monthly_mask = (df.Fecha.dt.year == Dates.current_year) & (df.Fecha.dt.month == Dates.current_month)
    # ? Yearly masks
    previous_yearly_mask = df.Fecha.dt.strftime('%Y') == Dates.previous_date.strftime('%Y')
    current_yearly_mask = df.Fecha.dt.strftime('%Y') == Dates.current_date.strftime('%Y')

    # ? Monthly masks
    previous_monthly_mask = df.Fecha.dt.strftime('%m-%Y') == Dates.previous_date.strftime('%m-%Y')
    current_monthly_mask = df.Fecha.dt.strftime('%m-%Y') == Dates.current_date.strftime('%m-%Y')

    # ? Daily masks
    previous_daily_mask = df.Fecha.dt.strftime('%d-%m-%Y') == Dates.previous_date.strftime('%d-%m-%Y')
    current_daily_mask = df.Fecha.dt.strftime('%d-%m-%Y') == Dates.current_date.strftime('%d-%m-%Y')

  return Masks
