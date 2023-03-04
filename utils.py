import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet():
  creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json')
  client = gspread.authorize(creds)
  sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1rYSBpWhHJuHlqCQzFuj99CEoZvCmPDUxWD54Ki7eolg').sheet1
  
  return sheet
