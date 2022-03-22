import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

def connect_gspread(jsonf, key, title):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(title)
    return worksheet

def new_gspread(jsonf, key, title):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).add_worksheet(title=title, rows=500, cols=30)
    return worksheet

def update_title(title, spread_sheet_key):
    jsonf = "bin-bib-record-500974b2ae26.json"
    ws = connect_gspread(jsonf,spread_sheet_key, title)
    ws.update_title(title)

def new_worksheet(title, spread_sheet_key):
    jsonf = "bin-bib-record-500974b2ae26.json"
    ws = new_gspread(jsonf, spread_sheet_key, title)

def update(position, tp, spread_sheet_key, title):
    jsonf = "bin-bib-record-500974b2ae26.json"
    ws = connect_gspread(jsonf,spread_sheet_key, title)

    for i in range(len(tp)):
        ws.update_cell(position, i+1, tp[i])



