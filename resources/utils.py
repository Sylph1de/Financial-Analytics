from os import environ, getenv

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet():
  gcp_keys = [key for key in environ.keys() if key.startswith('PROJECT_GCP_')]
  gcp_data = {key.replace('PROJECT_GCP_', '').lower(): environ.get(key) for key in gcp_keys}
  creds = ServiceAccountCredentials.from_json_keyfile_dict(gcp_data)
  client = gspread.authorize(creds)
  sheet = client.open_by_url(getenv('SHEET_URL')).sheet1
  return sheet
