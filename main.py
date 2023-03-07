from os import getenv
from warnings import filterwarnings

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from resources.add_data.add_data import get_add_data
from resources.analytics.ant_spending import get_ants
from resources.analytics.general import get_general
from resources.analytics.income import get_income
from resources.analytics.spending import get_spending
from resources.full_view.full_view import get_full_view
from resources.utils import get_sheet

load_dotenv()
filterwarnings('ignore')

# ? CONFIG
title = 'Finanzas'
st.set_page_config(
    page_title=title + ' - DEV' if getenv('DEV') else title,
    page_icon=':money_with_wings:',
    layout='wide',
    menu_items={
        "Get help": None,
        "Report a Bug": None,
    },
)
st.title(':red[Finanzas]')
with st.columns(5)[0]:
    st.session_state.name = st.text_input('Name', placeholder='Nombre', label_visibility='collapsed')
    st.session_state.pin = st.text_input('Pin', placeholder='PIN', max_chars=4, label_visibility='collapsed', type='password')
if st.session_state.name and st.session_state.pin:
    sheet = get_sheet()
    if sheet:
        records = sheet.get_all_records()
        df = pd.DataFrame(records)

        # ? TRANSFORMATION
        try:
            df.Gasto = df.Gasto.astype(float).apply(lambda x: round(x, 2))
            df.Ingreso = df.Ingreso.astype(float).apply(lambda x: round(x, 2))
            df.Fecha = pd.to_datetime(df.Fecha, format='%d/%m/%Y')
        except Exception:
            pass

        # ? LAYOUT
        analytics, full_view, add_data = st.tabs(['Análisis', 'Vista previa', 'Agregar registro'])

        with analytics:
            try:
                with st.expander('**General**', expanded=True):
                    get_general(df)

                columns = st.columns(3)

                with columns[0]:
                    with st.expander('**Gastos hormiga**', expanded=True):
                        get_ants(df)

                with columns[1]:
                    with st.expander('**Gastos**', expanded=True):
                        get_spending(df)

                with columns[2]:
                    with st.expander('**Ingresos**', expanded=True):
                        get_income(df)
            except Exception:
                st.info('Aún no tenés los suficientes registros para poder hacer un análisis', icon='😔')

        with full_view:
            get_full_view(df)

        with add_data:
            columns = st.columns([1, 3, 1])

            with columns[1]:
                get_add_data()

        # with remove_data:
        #     columns = st.columns([1, 1, 4, 2, 1.5, 1.5, 4])
        #     for i, col in enumerate(df.columns, start=1):
        #         with columns[i]:
        #             st.markdown(col)
        #     with columns[0]:
        #         st.markdown('Acción')
        #     for i, element in enumerate(df.to_dict('records')):
        #         with columns[0]:
        #             st.button('Delete')
        #         with columns[1]:
        #             st.markdown(element['Fecha'].strftime('%d-%b-%Y'))
        #     with columns[-1]:
        #         st.button('Eliminar registros seleccionados')
