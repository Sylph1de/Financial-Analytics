import streamlit as st

from resources.data.dates import get_dates
from resources.data.masks import get_masks
from resources.tools import cash, month


def get_spending(parsed_df):
  Dates = get_dates()
  Masks = get_masks(parsed_df)

  # ? Yearly spending
  previous_year_spent = parsed_df[Masks.previous_yearly_mask].Gasto.sum()
  current_year_spent = parsed_df[Masks.current_yearly_mask].Gasto.sum()
  delta_year_spent = current_year_spent - previous_year_spent

  # ? Monthly spending
  previous_month_spent = parsed_df[Masks.previous_monthly_mask].Gasto.sum()
  current_month_spent = parsed_df[Masks.current_monthly_mask].Gasto.sum()
  delta_month_spent = current_month_spent - previous_month_spent

  # ? Daily spending
  # FIXME
  previous_day_spent = parsed_df[Masks.previous_daily_mask].Gasto.sum()
  current_day_spent = parsed_df[Masks.current_daily_mask].Gasto.sum()
  delta_day_spent = previous_day_spent - current_day_spent

  columns = st.columns(3)
  with columns[0]:
    st.subheader(':red[Anual]')
    st.metric('Año anterior (%s)' % Dates.previous_year, cash(previous_year_spent))
    st.metric('Este año (%s)' % Dates.current_year, cash(current_year_spent), delta=cash(delta_year_spent), delta_color='inverse')
  with columns[1]:
    st.subheader(':red[Mensual]')
    st.metric('Mes anterior (%s)' % month(Dates.previous_month), cash(previous_month_spent))
    st.metric('Este mes (%s)' % month(Dates.current_month), cash(current_month_spent), delta=cash(delta_month_spent), delta_color='inverse')
  with columns[2]:
    st.subheader(':red[Diario]')
    st.metric('Ayer (%s)' % Dates.previous_date.strftime('%d-%b-%Y'), cash(previous_month_spent))
    st.metric('Hoy (%s)' % Dates.current_date.strftime('%d-%b-%Y'), cash(current_month_spent), delta=cash(delta_day_spent), delta_color='inverse')
