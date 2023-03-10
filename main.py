from os import getenv
from warnings import filterwarnings

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml
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
name = st.session_state.get('name')
sheet_url = st.session_state.get('sheet_url')
if name:
    title += ' (%s)' % name
st.set_page_config(
    page_title=title + ' - DEV' if getenv('DEV') else title,
    page_icon=':money_with_wings:',
    layout='wide',
    menu_items={
        "Get help": None,
        "Report a Bug": None,
        "About": sheet_url
    },
)
upper_columns = st.columns(3)
with upper_columns[0]:
    st.title(f':red[{title}]')
with open('./config.yaml', 'r') as f:
  config = yaml.load(f, Loader=yaml.loader.SafeLoader)
  cookie = config.get('cookie')



auth = stauth.Authenticate(
  config.get('credentials'),
  cookie.get('name'),
  cookie.get('key'),
  cookie.get('expiry_days')
)
main_columns = st.columns(3)
with main_columns[0]:
    name, status, username = auth.login('Iniciar sesión', 'main')
if status:
    with upper_columns[0]:
        auth.logout('Cerrar sesión', 'main')
    sheet = get_sheet(config, username)
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
            except Exception as e:
                st.info('Aún no tenés los suficientes registros para poder hacer un análisis', icon='😔')

        with full_view:
            get_full_view(df)

        with add_data:
            columns = st.columns([1, 3, 1])

            with columns[1]:
                get_add_data(config, username)
elif status == False:
    with main_columns[0]:
        st.error('Nombre/Contraseña incorrecto', icon='❌')
