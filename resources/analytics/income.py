import streamlit as st

from resources.data.dates import get_dates
from resources.data.masks import get_masks
from resources.tools import cash, month


def get_income(parsed_df):
  Masks = get_masks(parsed_df)
  Dates = get_dates()

  # ? Yearly income
  previous_year_income = parsed_df[Masks.previous_yearly_mask].Ingreso.sum()
  current_year_income = parsed_df[Masks.current_yearly_mask].Ingreso.sum()
  delta_year_income = current_year_income - previous_year_income

  # ? Monthly income
  previous_month_income = parsed_df[Masks.previous_monthly_mask].Ingreso.sum()
  current_month_income = parsed_df[Masks.current_monthly_mask].Ingreso.sum()
  delta_month_income = current_month_income - previous_month_income

  # ? Daily income
  previous_day_income = parsed_df[Masks.previous_daily_mask].Ingreso.sum()
  current_day_income = parsed_df[Masks.current_daily_mask].Ingreso.sum()
  delta_day_income = current_day_income - previous_day_income

  columns = st.columns(3)
  with columns[0]:
    st.subheader(':green[Anual]')
    st.metric('Año anterior (%s)' % Dates.previous_year, cash(previous_year_income))
    st.metric('Este año (%s)' % Dates.current_year, cash(current_year_income), delta=cash(delta_year_income))
  with columns[1]:
    st.subheader(':green[Mensual]')
    st.metric('Mes anterior (%s)' % month(Dates.previous_month), cash(previous_month_income))
    st.metric('Este mes (%s)' % month(Dates.current_month), cash(current_month_income), delta=cash(delta_month_income))
  with columns[2]:
    st.subheader(':green[Diario]')
    st.metric('Ayer (%s)' % Dates.previous_date.strftime('%d-%b-%Y'), cash(previous_day_income))
    st.metric('Hoy (%s)' % Dates.current_date.strftime('%d-%b-%Y'), cash(current_day_income), delta=cash(delta_day_income))
