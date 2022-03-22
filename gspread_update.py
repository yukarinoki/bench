import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    return worksheet

def update(position, tp):
    jsonf = "bin-bib-record-500974b2ae26.json"
    spread_sheet_key = "1x2bjNSs2yvSzVosxJWVRRQ36OLUKVjEoy7rM5WhIumw"
    ws = connect_gspread(jsonf,spread_sheet_key)

    for i in range(len(tp)):
        ws.update_cell(position, i+1, tp[i])



