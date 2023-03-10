from os import getenv

import streamlit as st
from cryptography.fernet import Fernet
from streamlit_authenticator import Hasher
from dotenv import load_dotenv

load_dotenv()

from math import log, floor


def human_format(number):
  number = int(number) if number % 1 == 0 else round(number, 2)
  k = 1000.0
  if number >= k:
    units = ['', 'K', 'M', 'G', 'T', 'P']
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])
  return number

def cash(amount, mode=None):
  if mode == 'delta' and amount == 0:
    return None
  if amount >= 0:
    return '$ %s' % human_format(amount)
  else:
    return '-$ %s' % human_format(amount*-1)


def month(value):
  month_list = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  return month_list[value-1]


def notify(container, mode: str, **kwargs):

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
  sheet_bytes = config.get('credentials').get('usernames').get(username).get('sheet_url').encode('utf-8')
  key = getenv('FERNET_KEY')
  fernet = Fernet(key)
  sheet_url = fernet.decrypt(sheet_bytes).decode('utf-8')
  st.session_state.sheet_url = sheet_url
  return sheet_url

def encrypt_sheet_url(url):
  key = getenv('FERNET_KEY')
  fernet = Fernet(key)
  encrypted_sheet_url = fernet.encrypt(url.encode('utf-8')).decode('utf-8')
  return encrypted_sheet_url

def hash_pwd(pwd):
  hashed_pwd = Hasher([pwd]).generate().pop(0)
  return hashed_pwd
