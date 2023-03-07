from os import environ, getenv

import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet():
  gcp_keys = [key for key in environ.keys() if key.startswith('PROJECT_GCP_')]
  gcp_data = {key.replace('PROJECT_GCP_', '').lower(): environ.get(key) for key in gcp_keys}
  creds = ServiceAccountCredentials.from_json_keyfile_dict(gcp_data)
  client = gspread.authorize(creds)
  name = st.session_state.get('name', default='empty').upper()
  pin = st.session_state.get('pin', default='empty')
  if pin == getenv(name+'_PIN'):
    sheet_url = getenv(name+'_SHEET_URL')
    sheet = client.open_by_url(sheet_url).sheet1
    return sheet
