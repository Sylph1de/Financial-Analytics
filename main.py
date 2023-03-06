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
# ? TRANSFORMATION
df.Gasto = df.Gasto.astype(float).apply(lambda x: round(x, 2))
df.Ingreso = df.Ingreso.astype(float).apply(lambda x: round(x, 2))

df.Fecha = pd.to_datetime(df.Fecha, format='%d/%m/%Y')

# ? LAYOUT
analytics, full_view, add_data = st.tabs(['Análisis', 'Vista previa', 'Agregar registro'])

with analytics:

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

with full_view:
    get_full_view(df)

with add_data:
    columns = st.columns([1, 3, 1])

    with columns[1]:
        get_add_data()
