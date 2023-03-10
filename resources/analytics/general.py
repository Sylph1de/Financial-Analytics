import plotly.express as px
import streamlit as st

from resources.data.dates import get_dates
from resources.data.masks import get_masks
from resources.tools import cash, month


def get_general(__df):
  Masks = get_masks(__df)
  Dates = get_dates()
  main_columns = st.columns([1, 2])
  with main_columns[0]:
    st.subheader('Ganancias')
    columns = st.columns(2)
    yearly = __df[Masks.current_yearly_mask]
    yearly_incomes = yearly.groupby(yearly.Fecha.dt.month).Ingreso.sum().mean()
    yearly_spent = yearly.groupby(yearly.Fecha.dt.month).Gasto.sum().mean()
    yearly_earnings = yearly_incomes - yearly_spent
    with columns[0]:
        st.metric(':%s[__Ganancia anual (%s)__]' % ('green' if yearly_earnings >= 0 else 'red', Dates.current_year), cash(yearly_earnings))

    monthly = __df[Masks.current_monthly_mask]
    monthly_incomes = monthly.Ingreso.sum()
    monthly_spent = monthly.Gasto.sum()
    monthly_earnings = monthly_incomes - monthly_spent
    with columns[1]:
        st.metric(':%s[__Ganancia mensual (%s)__]' % ('green' if monthly_earnings >= 0 else 'red', month(Dates.current_month)), cash(monthly_earnings))
    st.subheader('Promedios')

    current_monthly_income_mean = yearly.groupby(yearly.Fecha.dt.month).Ingreso.sum().mean()
    current_monthly_spent_mean = yearly.groupby(yearly.Fecha.dt.month).Gasto.sum().mean()

    columns = st.columns(2)
    with columns[0]:
        st.metric(':red[__Promedio gasto mensual (%s)__]' % Dates.current_year, cash(current_monthly_spent_mean))
    with columns[1]:
        st.metric(':green[__Promedio ingreso mensual (%s)__]' % Dates.current_year, cash(current_monthly_income_mean))

  with main_columns[1]:
      columns = st.columns(2)
      with columns[0]:
          data = yearly[yearly.Tipo != 'Ingreso']
          if not data.empty:
              st.subheader('Porcentaje de gastos mensuales por tipo')
              fig = px.pie(data, names='Tipo', labels='Tipo', values='Gasto', height=250)
              fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
              st.plotly_chart(fig, use_container_width=True)

      with columns[1]:
          data = __df.drop(__df[~Masks.current_yearly_mask].index)
          if not data.empty:
              data.Fecha = data.Fecha.apply(lambda x: month(x.month))
              data = data.groupby(data.Fecha).Ingreso.sum()
              fig = px.bar(data, x=data.index, y=data.values, color=data.index, labels={'y': 'Ingreso', 'Fecha': 'Mes'}, height=250)

              st.subheader('Ingresos mensuales (%s)' % Dates.current_year)
              fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
              st.plotly_chart(fig, use_container_width=True)
