from os import environ, getenv

import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet():
  gcp_keys = [key for key in environ.keys() if key.startswith('PROJECT_GCP_')]
  gcp_data = {key.replace('PROJECT_GCP_', '').lower(): environ.get(key) for key in gcp_keys}
  creds = ServiceAccountCredentials.from_json_keyfile_dict(gcp_data)
  client = gspread.authorize(creds)
  pin = st.session_state.pin
  if pin == getenv('LAURA_PIN'):
    sheet_url = getenv('LAURA_SHEET_URL')
  elif pin == getenv('FRANCO_PIN'):
    sheet_url = getenv('FRANCO_SHEET_URL')
  elif pin == getenv('WALTER_PIN'):
    sheet_url = getenv('WALTER_SHEET_URL')
  elif pin == getenv('TEST_PIN'):
    sheet_url = getenv('TEST_SHEET_URL')
  sheet = client.open_by_url(sheet_url).sheet1
  return sheet
