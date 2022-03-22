import argparse    # 1. argparseをインポート
import subprocess
from datetime import datetime as dt
import json
import re
import csv
import gspread_update
import time

def get_githash():
    git_result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
    if git_result.returncode != 0:
         raise AssertionError("is this git repository ?")
    return git_result.stdout[0:7]

def get_timeofday():
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y%m%d%S')
    return tstr


parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('file', help='benchmark result file')    # 必須の引数を追加
parser.add_argument('--spreadsheet', help='key of spreadsheet')    # オプション引数（指定しなくても良い引数）を追加
parser.add_argument('--csv', help='csv', action="store_true")   # よく使う引数なら省略形があると使う時に便利

args = parser.parse_args()    # 4. 引数を解析



title = get_timeofday() + "_" + get_githash()
with open('benchmark-settings.json') as f:
    jsn = json.load(f)

column_length = jsn['column_length']
result = [jsn['column_name']]

file = args.file

state = 0
pos = 1
reglen = jsn["regexp"]['length']
result.append([])
with open(file, 'r') as f:
    file_data = f.readlines()
    for line in file_data:
        r = jsn["regexp"]["regexps"][state]["regexp"]
        len = jsn["regexp"]["regexps"][state]["groups"]

        m = re.match(r, line)

        if m :
            for i in range(1, len+1):
                result[pos].append(m.group(i))
            
            state = state + 1
            if state == reglen:
                state = 0
                result.append([])
                pos = pos + 1

if result[pos] == []:
    result.pop(pos)


if None == args.spreadsheet and not args.csv:
    print(result)

if args.spreadsheet:
    sk = args.spreadsheet
    gspread_update.new_worksheet(title, sk)
    for i, r in enumerate(result):
        gspread_update.update(i+1, r, sk, title)
        time.sleep(5)

if args.csv:
    with open(title + ".csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(result)
    
