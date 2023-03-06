import streamlit as st

from resources.data.dates import get_dates
from resources.data.masks import get_masks
from resources.tools import cash, month


def get_ants(__df):
  Dates = get_dates()
  Masks = get_masks(__df)
  ant_spending = __df[(__df.Gasto <= 200) & (__df.Gasto >= 1)]

  # ? Yearly ant spending
  previous_year_ant_spending = ant_spending[Masks.previous_yearly_mask].Gasto.sum()
  current_year_ant_spending = ant_spending[Masks.current_yearly_mask].Gasto.sum()
  delta_year_ant_spending = current_year_ant_spending - previous_year_ant_spending

  # ? Monthly ant spending
  previous_month_ant_spending = ant_spending[Masks.previous_monthly_mask].Gasto.sum()
  current_month_ant_spending = ant_spending[Masks.current_monthly_mask].Gasto.sum()
  delta_month_ant_spending = current_month_ant_spending - previous_month_ant_spending

  # ? Daily ant spending
  previous_day_ant_spending = ant_spending[Masks.previous_daily_mask].Gasto.sum()
  current_day_ant_spending = ant_spending[Masks.current_daily_mask].Gasto.sum()
  delta_day_ant_spending = current_day_ant_spending - previous_day_ant_spending

  columns = st.columns(3)
  with columns[0]:
      st.subheader(':red[Anual]')
      st.metric('Año anterior (%s)' % Dates.previous_year, cash(previous_year_ant_spending))
      st.metric('Este año (%s)' % Dates.current_year, cash(current_year_ant_spending), delta=cash(delta_year_ant_spending), delta_color='inverse')
  with columns[1]:
      st.subheader(':red[Mensual]')
      st.metric('Mes anterior (%s)' % month(Dates.previous_month), cash(previous_month_ant_spending))
      st.metric('Este mes (%s)' % month(Dates.current_month), cash(current_month_ant_spending), delta=cash(delta_month_ant_spending), delta_color='inverse')
  with columns[2]:
      st.subheader(':red[Diario]')
      st.metric('Ayer (%s)' % Dates.previous_date.strftime('%d-%b-%Y'), cash(previous_day_ant_spending))
      st.metric('Hoy (%s)' % Dates.current_date.strftime('%d-%b-%Y'), cash(current_day_ant_spending), delta=cash(delta_day_ant_spending), delta_color='inverse')
