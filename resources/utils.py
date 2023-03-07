from os import environ

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from resources.tools import get_sheet_url


def get_sheet(config, username):
  gcp_keys = [key for key in environ.keys() if key.startswith('PROJECT_GCP_')]
  gcp_data = {key.replace('PROJECT_GCP_', '').lower(): environ.get(key) for key in gcp_keys}
  creds = ServiceAccountCredentials.from_json_keyfile_dict(gcp_data)
  client = gspread.authorize(creds)
  sheet_url = get_sheet_url(config, username)
  sheet = client.open_by_url(sheet_url).sheet1
  return sheet
