from datetime import datetime, timedelta
from warnings import filterwarnings

import pandas as pd
import streamlit as st
import plotly.express as px

from formatting_tools import cash, month, parse_mode
from utils import get_sheet

filterwarnings('ignore')

# ? CONFIG
st.set_page_config(
    page_title='Finanzas (Franco)',
    page_icon=':money_with_wings:',
    menu_items={
        "Get help": None,
        "Report a Bug": None,
        "About": None,
    },
)

columns = st.columns(3)
with columns[0]:
    st.title(':violet[Finanzas]')
with columns[1]:
    st.button('🔗')
sheet = get_sheet()
records = sheet.get_all_records()
df = pd.DataFrame(records)
parsed_df = df.copy()

# ? TRANSFORMATION
parsed_df.Gasto = parsed_df.Gasto.astype(float).apply(lambda x: round(x,2))
parsed_df.Ingreso = parsed_df.Ingreso.astype(float).apply(lambda x: round(x,2))
parsed_df.Fecha = pd.to_datetime(parsed_df.Fecha, format='%d/%m/%Y')

# ? LAYOUT
analytics, full_view, add_data = st.tabs(['Analytics', 'Full view', 'Add data'])

current_date = datetime.now()
previous_date = current_date - timedelta(1)
current_year = current_date.year
previous_year = current_date.year - 1
current_month = current_date.month
previous_month = current_month - 1 if current_month != 1 else 12
current_day = current_date.day
previous_day = previous_date.day

with analytics:
    # ? Yearly masks
    previous_yearly_mask = parsed_df.Fecha.dt.year == previous_year
    current_yearly_mask = parsed_df.Fecha.dt.year == current_year
    
    # ? Monthly masks
    previous_monthly_mask = (parsed_df.Fecha.dt.year == current_year) & (parsed_df.Fecha.dt.month == previous_month)
    current_monthly_mask = (parsed_df.Fecha.dt.year == current_year) & (parsed_df.Fecha.dt.month == current_month)
    
    # ? Daily masks
    previous_daily_mask = parsed_df.Fecha.dt.strftime('%d-%m-%Y') == previous_date.strftime('%d-%m-%Y')
    current_daily_mask = parsed_df.Fecha.dt.strftime('%d-%m-%Y') == current_date.strftime('%d-%m-%Y')
    
    with st.expander('**General**', expanded=True):
        st.subheader('Ganancias')
        columns = st.columns(2)
        yearly_incomes = parsed_df[current_yearly_mask].Ingreso.sum()
        yearly_spent = parsed_df[current_yearly_mask].Gasto.sum()
        yearly_earnings = yearly_incomes - yearly_spent
        with columns[0]:
            st.metric(':%s[__Ganancia anual (%s)__]' % ('green' if yearly_earnings >= 0 else 'red', current_year), cash(yearly_earnings))
        
        monthly_incomes = parsed_df[current_monthly_mask].Ingreso.sum()
        monthly_spent = parsed_df[current_monthly_mask].Gasto.sum()
        monthly_earnings = monthly_incomes - monthly_spent
        with columns[1]:
            st.metric(':%s[__Ganancia mensual (%s)__]' % ('green' if monthly_earnings >= 0 else 'red', month(current_month)), cash(monthly_earnings))
        st.subheader('Promedios')
        
        current_monthly_income_mean = parsed_df[current_yearly_mask]
        current_monthly_income_mean.Fecha = current_monthly_income_mean.Fecha.apply(lambda x: x.month)
        current_monthly_income_mean = current_monthly_income_mean.groupby('Fecha').Ingreso.sum().mean()
        
        current_monthly_spent_mean = parsed_df[current_yearly_mask]
        current_monthly_spent_mean.Fecha = current_monthly_spent_mean.Fecha.apply(lambda x: x.month)
        current_monthly_spent_mean = current_monthly_spent_mean.groupby('Fecha').Gasto.sum().mean()
        
        columns = st.columns(2)
        with columns[0]:
            st.metric(':red[__Promedio gasto mensual (%s)__]' % current_year, cash(current_monthly_spent_mean))
        with columns[1]:
            st.metric(':green[__Promedio ingreso mensual (%s)__]' % current_year, cash(current_monthly_income_mean))
        
        
        data = parsed_df.drop(parsed_df[parsed_df.Tipo.str.contains('Ingreso')].index)[current_monthly_mask]
        if not data.empty:
            fig = px.pie(data, names='Tipo')
            
            st.markdown('---')
            st.subheader('Porcentaje de gastos mensuales por categoría')
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        data = parsed_df.drop(parsed_df[~current_yearly_mask].index)
        if not data.empty:
            data.Fecha = data.Fecha.apply(lambda x: month(x.month))
            data = data.groupby(['Fecha']).Ingreso.sum()
            fig = px.bar(data, x=data.index, y=data.values, color=data.index, labels={'y': 'Ingreso', 'Fecha': 'Mes'})
            
            st.markdown('---')
            st.subheader('Ingresos mensuales (%s)' % current_year)
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

    with st.expander('**Gastos hormiga**', expanded=True):
        ant_spending = parsed_df[(parsed_df.Gasto <= 200) & (parsed_df.Gasto >= 1)]
        
        # ? Yearly ant spending
        previous_year_ant_spending = ant_spending[previous_yearly_mask].Gasto.sum()
        current_year_ant_spending = ant_spending[current_yearly_mask].Gasto.sum()
        delta_year_ant_spending = current_year_ant_spending - previous_year_ant_spending
        
        # ? Monthly ant spending
        previous_month_ant_spending = ant_spending[previous_monthly_mask].Gasto.sum()
        current_month_ant_spending = ant_spending[current_monthly_mask].Gasto.sum()
        delta_month_ant_spending = current_month_ant_spending - previous_month_ant_spending
        
        # ? Daily ant spending
        previous_day_ant_spending = ant_spending[previous_daily_mask].Gasto.sum()
        current_day_ant_spending = ant_spending[current_daily_mask].Gasto.sum()
        delta_day_ant_spending = current_day_ant_spending - previous_day_ant_spending
        
        columns = st.columns(3)
        with columns[0]:
            st.subheader(':red[Anual]')
            st.metric('Año anterior (%s)' % previous_year, cash(previous_year_ant_spending))
            st.metric('Este año (%s)' % current_year, cash(current_year_ant_spending), delta=cash(delta_year_ant_spending), delta_color='inverse')
        with columns[1]:
            st.subheader(':red[Mensual]')
            st.metric('Mes anterior (%s)' % month(previous_month), cash(previous_month_ant_spending))
            st.metric('Este mes (%s)' % month(current_month), cash(current_month_ant_spending), delta=cash(delta_month_ant_spending), delta_color='inverse')
        with columns[2]:
            st.subheader(':red[Diario]')
            st.metric('Ayer (%s)' % previous_date.strftime('%d-%b-%Y'), cash(previous_day_ant_spending))
            st.metric('Hoy (%s)' % current_date.strftime('%d-%b-%Y'), cash(current_day_ant_spending), delta=cash(delta_day_ant_spending), delta_color='inverse')
            
    with st.expander('**Gastos**', expanded=True):
        # ? Yearly spending
        previous_year_spent = parsed_df[previous_yearly_mask].Gasto.sum()
        current_year_spent = parsed_df[current_yearly_mask].Gasto.sum()
        delta_year_spent = current_year_spent - previous_year_spent
        
        # ? Monthly spending
        previous_month_spent = parsed_df[previous_monthly_mask].Gasto.sum()
        current_month_spent = parsed_df[current_monthly_mask].Gasto.sum()
        delta_month_spent = current_month_spent - previous_month_spent
        
        # ? Daily spending
        previous_day_spent = parsed_df[previous_daily_mask].shape[0]
        current_day_spent = parsed_df[current_daily_mask].shape[0]
        delta_day_spent = current_day_spent - previous_day_spent

        columns = st.columns(3)
        with columns[0]:
            st.subheader(':red[Anual]')
            st.metric('Año anterior (%s)' % previous_year,
                    cash(previous_year_spent))
            st.metric('Este año (%s)' % current_year,
                    cash(current_year_spent), delta=cash(delta_year_spent), delta_color='inverse')
        with columns[1]:
            st.subheader(':red[Mensual]')
            st.metric('Mes anterior (%s)' % month(previous_month),
                    cash(previous_month_spent))
            st.metric('Este mes (%s)' % month(current_month),
                    cash(current_month_spent), delta=cash(delta_month_spent), delta_color='inverse')
        with columns[2]:
            st.subheader(':red[Diario]')
            st.metric('Ayer (%s)' % previous_date.strftime('%d-%b-%Y'),
                    cash(previous_month_spent))
            st.metric('Hoy (%s)' % current_date.strftime('%d-%b-%Y'),
                    cash(current_month_spent), delta=cash(delta_month_spent), delta_color='inverse')
            
    with st.expander('**Ingresos**', expanded=True):
        # ? Yearly income
        previous_year_income = parsed_df[previous_yearly_mask].Ingreso.sum()
        current_year_income = parsed_df[current_yearly_mask].Ingreso.sum()
        delta_year_income = current_year_income - previous_year_income
        
        # ? Monthly income
        previous_month_income = parsed_df[previous_monthly_mask].Ingreso.sum()
        current_month_income = parsed_df[current_monthly_mask].Ingreso.sum()
        delta_month_income = current_month_income - previous_month_income
        
        # ? Daily income
        previous_day_income = parsed_df[previous_daily_mask].Ingreso.sum()
        current_day_income = parsed_df[current_daily_mask].Ingreso.sum()
        delta_day_income = current_day_income - previous_day_income

        columns = st.columns(3)
        with columns[0]:
            st.subheader(':green[Anual]')
            st.metric('Año anterior (%s)' % previous_year,
                    cash(previous_year_income))
            st.metric('Este año (%s)' % current_year,
                    cash(current_year_income), delta=cash(delta_year_income))
        with columns[1]:
            st.subheader(':green[Mensual]')
            st.metric('Mes anterior (%s)' % month(previous_month),
                    cash(previous_month_income))
            st.metric('Este mes (%s)' % month(current_month),
                    cash(current_month_income), delta=cash(delta_month_income))
        with columns[2]:
            st.subheader(':green[Diario]')
            st.metric('Ayer (%s)' % previous_date.strftime('%d-%b-%Y'),
                    cash(previous_day_income))
            st.metric('Hoy (%s)' % current_date.strftime('%d-%b-%Y'),
                    cash(current_day_income), delta=cash(delta_day_income))

with full_view:
    st.subheader('Ordenamiento')
    sorting = st.radio('Ordenamiento', parsed_df.columns, label_visibility='collapsed', horizontal=True)
    is_asc = st.checkbox('Ascendente', value=True)
    st.subheader('Filtrado')
    columns = st.columns(3)
    with columns[0]:
        column = st.selectbox('Columna', [None, *parsed_df.columns])
        filter_button = st.button('__Filtrar__', type='secondary')
    query_result = parsed_df.copy()
    query_result.sort_values(by=sorting, ascending=is_asc, inplace=True)
    if column is not None:
        sample = parsed_df[column].tolist()[0]
        with columns[1]:
            if isinstance(sample, int) or isinstance(sample, float):
                options = ['==', '!=', '<', '>', '<=', '>=']
            elif isinstance(sample, str):
                options = ['==', '!=', 'incluye', 'no incluye']
            else:
                options = ['==', '!=', '<', '>', '<=','<=']
            mode = st.selectbox('Operación', options, format_func=parse_mode)
        with columns[2]:
            if isinstance(sample, pd._libs.tslibs.timestamps.Timestamp):
                search_value = st.date_input(column, key='search_date')
            elif isinstance(sample, str):
                search_value = st.text_input(column, key='search_text')
            else:
                search_value = st.number_input(column, key='search_spend',
                                               min_value=float(parsed_df[column].min()), max_value=float(parsed_df[column].max()))
        if search_value != '' and filter_button:
            if mode == 'incluye':
                query_result = parsed_df[parsed_df[column].str.contains(search_value)]
            elif mode == 'no incluye':
                query_result = parsed_df[parsed_df[column].str.contains(search_value) == False]
            else:
                query_result = parsed_df.query(f'{column} {mode} @search_value')
    query_result.Fecha = query_result.Fecha.apply(lambda x: x.strftime('%d/%m/%Y'))
    query_result.Gasto = query_result.Gasto.astype(str).apply(lambda x: '$' + x)
    query_result.Ingreso = query_result.Ingreso.astype(str).apply(lambda x: '$' + x)
    # query_result.reset_index(inplace=True)
    # query_result.drop(query_result['index'].index)
    query_result = query_result.style.set_properties(**{'color': 'rgb(255, 115, 115)'}, subset=['Gasto'])
    query_result = query_result.set_properties(**{'color': 'rgb(115, 255, 115)'}, subset=['Ingreso'])
    query_result = query_result.set_properties(**{'color': 'cyan'}, subset=['Tipo'])
    st.table(query_result)
    # edited_data.Gasto = edited_data.Gasto.str.replace('$', '')
    # edited_data.Ingreso = edited_data.Ingreso.str.replace('$', '')
    # edited_data.Gasto = edited_data.Gasto.astype(float)
    # edited_data.Ingreso = edited_data.Ingreso.astype(float)
    # if st.button('Update table', type='primary'):
    #     print(edited_data)

with add_data:
    columns = st.columns(3)
    with columns[0]:
        date = st.date_input('Fecha').strftime('%d/%m/%Y')
    # with columns[1]:
    description = st.text_input('Descripción')
    with columns[1]:
        spent = st.number_input('Gasto', min_value=10.0)
    add_button = st.button('Agregar datos')
    if add_button:
        body = (date, description, '$ ' + str(spent).replace('.', ','))
        sheet.append_row(body)
        with columns[0]:
            st.success('Datos agregados')
            temp_df = pd.DataFrame([{col:value for col, value in zip(parsed_df.columns, body)}])
            st.table(temp_df)
