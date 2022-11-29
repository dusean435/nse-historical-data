import requests
from datetime import datetime, date
import re


ticker = 'SCOM'


today = date.today()
start_date = '01/01/1900'
end_date = today.strftime('%m/%d/%Y')

headers = {
      'Accept': '*/*',
      'User-Agent': 'NSE-HISTORICAL-DATA'
}

url = f'https://www.wsj.com/market-data/quotes/KE/XNAI/{ticker}/historical-prices/download?MOD_VIEW=page&num_rows=10000&startDate={start_date}&endDate={end_date}'
res = requests.get(url, headers=headers)
content = res.content.decode()
content = content.split('\n')

out_file = f'SCOM_{start_date}_{end_date}.csv'
path = out_file.replace('/', '-')

with open(path, "w") as f:
  f.write('Date,Open,High,Low,Close,Volume\n')

  data = content[1:]
  for idx, line in enumerate(data):
    old_date = line.split(',')[0]
    if re.match(r'\d+/\d+/\d+', old_date):
      new_date = datetime.strptime(old_date, '%m/%d/%y')
      line = line.replace(old_date, new_date.strftime('%Y/%m/%d'))
      data[idx] = line.replace(' ', '')+'\n'
  
  data.sort(key=lambda x: x.split()[0])
  f.writelines(data)

