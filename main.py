from datetime import datetime, timedelta
import json
from os import getenv
from warnings import filterwarnings

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from streamlit_elements import nivo, elements

from formatting_tools import cash, month, parse_mode
from utils import get_sheet

load_dotenv()
filterwarnings('ignore')

# ? CONFIG
st.set_page_config(
    page_title='Finanzas (Franco) - DEV' if getenv('DEV') else 'Finanzas (Franco)',
    page_icon=':money_with_wings:',
    layout='wide',
    menu_items={
        "Get help": None,
        "Report a Bug": None,
        "About": 'Sheet:\n'+getenv('SHEET_URL'),
    },
)

sheet = get_sheet()
records = sheet.get_all_records()
df = pd.DataFrame(records)
parsed_df = df.copy()

# ? TRANSFORMATION
parsed_df.Gasto = parsed_df.Gasto.astype(float).apply(lambda x: round(x, 2))
parsed_df.Ingreso = parsed_df.Ingreso.astype(float).apply(lambda x: round(x, 2))
parsed_df.Fecha = pd.to_datetime(parsed_df.Fecha, format='%d/%m/%Y')

# ? LAYOUT
analytics, full_view, add_data = st.tabs(['Análisis', 'Vista previa', 'Agregar registro'])

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
        main_columns = st.columns([1,2])
        with main_columns[0]:
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
        
        with main_columns[1]:
            columns = st.columns(2)
            with columns[0]:
                data = parsed_df[current_yearly_mask][parsed_df.Tipo != 'Ingreso']['Tipo']
                if not data.empty:
                    st.subheader('Porcentaje de gastos mensuales por tipo')
                    # with elements('piechart'):
                    #     nivo.Pie(
                    #         margin={ 'top': 40, 'right': 80, 'bottom': 80, 'left': 80 },
                    #         data=data.to_dict('records'),
                    #         id='Tipo',
                    #         value='Tipo',
                    #         innerRadius=0.5,
                    #         cornerRadius=10,
                    #         padAngle=0.5,
                    #         motionConfig="wobbly",
                    #         activeOuterRadiusOffset=8,
                    #         arcLinkLabel = 'id',
                    #         arcLinkLabelsSkipAngle={10},
                    #         arcLinkLabelsTextColor="white",
                    #         arcLinkLabelsThickness=2,
                    #         arcLinkLabelsColor={ 'from': 'color', 'modifiers': [] },
                    #         arcLabelsSkipAngle=10,
                    #         borderWidth=1
                    #         )
                    fig = px.pie(data, names='Tipo', height=250)
                    
                    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
            
            with columns[1]:
                data = parsed_df.drop(parsed_df[~current_yearly_mask].index)
                if not data.empty:
                    data.Fecha = data.Fecha.apply(lambda x: month(x.month))
                    data = data.groupby(['Fecha']).Ingreso.sum()
                    fig = px.bar(data, x=data.index, y=data.values, color=data.index, labels={'y': 'Ingreso', 'Fecha': 'Mes'}, height=250)
                    
                    st.subheader('Ingresos mensuales (%s)' % current_year)
                    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                    
    main_columns = st.columns(3)

    with main_columns[0]:
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
            
    with main_columns[1]:
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
      
    with main_columns[2]:
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
    columns = st.columns([1,2])
    with columns[0]:
        exploring_df = parsed_df.copy(deep=True)
        with st.expander('Ordenamiento', expanded=True):
            # st.subheader('Ordenamiento')
            sorting = st.radio('Ordenamiento', parsed_df.columns, label_visibility='collapsed', horizontal=True)
            is_asc = st.checkbox('Ascendente', value=True)
            if st.button('Ordenar'):
                exploring_df.sort_values(by=sorting, ascending=is_asc, inplace=True)
        with st.expander('Filtrado', expanded=True):
            filtering_columns = st.multiselect('Columnas', options=parsed_df.columns)
            exclusive = st.checkbox('Excluyente', value=True)
            filters = dict()
            for col in filtering_columns:
                sample = exploring_df[col][0]
                if col == 'Fecha':
                    min_value = exploring_df[col].min()
                    max_value = exploring_df[col].max()
                    filters[col] = st.date_input(col, value=(min_value, max_value), min_value=min_value, max_value=max_value)
                elif isinstance(sample, str):
                    st.subheader(col)
                    uniques = exploring_df[col].unique()
                    filters[col] = st.multiselect(col, options=uniques, default=uniques)
                elif isinstance(sample, int):
                    min_value = int(exploring_df[col].min())
                    max_value = int(exploring_df[col].max())
                    filters[col] = st.slider(col, min_value=min_value, max_value=max_value, value=(min_value, max_value))
                elif isinstance(sample, float):
                    min_value = float(exploring_df[col].min())
                    max_value = float(exploring_df[col].max())
                    filters[col] = st.slider(col, min_value=min_value, max_value=max_value, value=(min_value, max_value))
            query_data = []
            for key, value in filters.items():
                sample = value[0]
                if isinstance(sample, str):
                    filter_str = f'{key}.isin({value})'
                elif isinstance(sample, (int, float)):
                    filter_str = f'({key} >= {value[0]} & {key} <= {value[1]})'
                else:
                    filter_str = f'({key} >= "{value[0]}" & {key} <= "{value[1]}")'
                query_data.append(filter_str)
            mode = ' & ' if exclusive else ' | '
            query = mode.join(query_data)
            if st.button('Filtrar'):
                if query != '':
                    exploring_df = exploring_df.query(query)
        exploring_df.Fecha = exploring_df.Fecha.apply(lambda x: x.to_pydatetime().date().strftime('%d-%b-%Y'))
        exploring_df.Gasto = exploring_df.Gasto.astype(str).apply(lambda x: '$' + x)
        exploring_df.Ingreso = exploring_df.Ingreso.astype(str).apply(lambda x: '$' + x)
        exploring_df = exploring_df.style.set_properties(**{'color': 'rgb(255, 115, 115)'}, subset=['Gasto'])
        exploring_df = exploring_df.set_properties(**{'color': 'rgb(115, 255, 115)'}, subset=['Ingreso'])
        exploring_df = exploring_df.set_properties(**{'color': 'cyan'}, subset=['Tipo'])
    with columns[1]:
        st.table(exploring_df)

with add_data:
    main_columns = st.columns([1, 3, 1])
    
    with main_columns[1]:
        with st.form('add_data_form', clear_on_submit=True):
            st.subheader(':violet[Nuevo registro]')
            form_data = dict()
            columns = st.columns([1,2])
            with columns[0]:
                form_data['Fecha'] = st.date_input('Fecha')
            with columns[1]:
                autocomplete = parsed_df.Concepto.unique()
                form_data['Concepto'] = st.text_input('Concepto')
            columns = st.columns(3)
            with columns[0]:
                options = sorted(['Ocio', 'Transporte', 'Ingreso', 'Comida', 'Servicio', 'Otros', 'Salida'])
                form_data['Tipo'] = st.selectbox(':blue[Tipo]', options=options)
            with columns[1]:
                form_data['Gasto'] = st.number_input(':red[Gasto]', step=0.1)
            with columns[2]:
                form_data['Ingreso'] = st.number_input(':green[Ingreso]', step=0.1)
            with columns[0]:
                if st.form_submit_button('Agregar registro', type='primary'):
                    pass
