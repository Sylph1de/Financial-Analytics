from os import getenv
from cryptography.fernet import Fernet


def cash(amount):
  if amount >= 0:
    return '$ %s' % round(amount, 2)
  else:
    return '-$ %s' % round(amount*-1, 2)


def month(value):
  month_list = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  return month_list[value-1]


def notify(container, mode: str, **kwargs):
  import streamlit as st

  toast = eval('st.'+mode)
  with container:
    toast(**kwargs)


def append_row(config, username, container, row):
  from resources.utils import get_sheet

  sheet = get_sheet(config, username)

  try:
    sheet.append_row(row, value_input_option='USER_ENTERED')
    notify(container, 'success', body='Registro agregado correctamente.', icon='✅')

  except Exception as e:
    notify(container, 'error', body='Error, por favor intente de nuevo más tarde.', icon='❗')
    notify(container, 'error', body=e, icon='❗')


def get_sheet_url(config, username):
  sheet_bytes = config.get('credentials').get('usernames').get(username).get('sheet_url').encode('utf8')
  key = getenv('FERNET_KEY')
  fernet = Fernet(key)
  return fernet.decrypt(sheet_bytes).decode('utf-8')
