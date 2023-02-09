import requests
import csv
import sqlite3
import time

with open("tickers.csv", "r") as file:
    reader = csv.reader(file)
    tickers = [row[0] for row in reader]

with open("apikey", "r") as file:
  API_KEY = file.read().strip()

i = 0

conn = sqlite3.connect("stock_info.db")
cursor = conn.cursor()

done = ['A', 'AA', 'AAC', 'AAC-WS', 'AACG', 'AACI', 'AACIU', 'AACIW', 'AADI', 'AAIC', 'AAIC-P-B', 'AAIC-P-C', 'AAIN', 'AAL', 'AAMC', 'AAME', 'AAN', 'AAOI', 'AAON', 'AAP', 'AAPL', 'AAT', 'AAU', 'AAWW', 'AB', 'ABB', 'ABBV', 'ABC', 'ABCB', 'ABCL', 'ABCM', 'ABEO', 'ABEV', 'ABG', 'ABGI', 'ABIO', 'ABM', 'ABNB', 'ABOS', 'ABR', 'ABR-P-D', 'ABR-P-E', 'ABR-P-F', 'ABSI', 'ABST', 'ABT', 'ABUS', 'ABVC', 'AC', 'ACA', 'ACAB', 'ACABU', 'ACABW', 'ACAC', 'ACACU', 'ACACW', 'ACAD', 'ACAH', 'ACAHU', 'ACAHW', 'ACAQ', 'ACAQ-U', 'ACAQ-WS', 'ACAX', 'ACAXR', 'ACAXU', 'ACAXW', 'ACB', 'ACBA', 'ACBAU', 'ACBAW', 'ACCD', 'ACCO', 'ACDC', 'ACDCW', 'ACDI', 'ACDI-U', 'ACEL', 'ACER', 'ACET', 'ACGL', 'ACGLN', 'ACGLO', 'ACGN', 'ACHC', 'ACHL', 'ACHR', 'ACHV', 'ACI', 'ACIU', 'ACIW', 'ACLS', 'ACLX', 'ACM', 'ACMR', 'ACN', 'ACNB', 'ACNT', 'ACON', 'ACONW', 'ACOR', 'ACP-P-A', 'ACQR', 'ACQRU', 'ACQRW', 'ACR', 'ACR-P-C', 'ACR-P-D', 'ACRE', 'ACRO', 'ACRO-U', 'ACRO-WS', 'ACRS', 'ACRV', 'ACRX', 'ACST', 'ACT', 'ACTG', 'ACU', 'ACVA', 'ACXP', 'ADAG', 'ADAL', 'ADALU', 'ADALW', 'ADAP', 'ADBE', 'ADC', 'ADC-P-A', 'AAC-U', 'ADCT', 'ADD', 'ADEA', 'ADER', 'ADERU', 'ADERW', 'ADES', 'ADEX', 'ADEX-U', 'ADEX-WS', 'ADI', 'ADIL', 'ADILW', 'ADM', 'ADMA', 'ADMP', 'ADN', 'ADNT', 'ADNWW', 'ADOC', 'ADOCR', 'ADOCW', 'ADP', 'ADPT', 'ADRA', 'ADRA-U', 'ADRA-WS', 'ADRT', 'ADRT-U', 'ADSE', 'ADSEW', 'ADSK', 'ADT', 'ADTH', 'ADTHW', 'ADTN', 'ADTX', 'ADUS', 'ADV', 'ADVM', 'ADXN', 'AE', 'AEAE', 'AEAEU', 'AEAEW', 'AEE', 'AEFC', 'AEG', 'AEHA', 'AEHAU', 'AEHAW', 'AEHL', 'AEHR', 'AEI', 'AEIS', 'AEL', 'AEL-P-A', 'AEL-P-B', 'AEM', 'AEMD', 'AENZ', 'AEO', 'AEP', 'AEPPZ', 'AER', 'AES', 'AESC', 'AEVA', 'AEVA-WS', 'AEY', 'AEYE', 'AEZS', 'AFAR', 'AFARU', 'AFARW', 'AFBI', 'AFCG', 'AFG', 'AFGB', 'AFGC', 'AFGD', 'AFGE', 'AFIB', 'AFL', 'AFMD', 'AFRI', 'AFRIW', 'AFRM', 'AFTR', 'AFTR-U', 'AFTR-WS', 'AFYA', 'AG', 'AGAC', 'AGAC-U', 'AGAE', 'AGBA', 'AGBAW', 'AGCO', 'AGE', 'AGEN', 'AGFS', 'AGFY', 'AGGR', 'AGGRU', 'AGGRW', 'AGI', 'AGIL', 'AGILW', 'AGIO', 'AGL', 'AGLE', 'AGM', 'AGM-A', 'AGM-P-C', 'AGM-P-D', 'AGM-P-E', 'AGM-P-F', 'AGM-P-G', 'AGMH', 'AGNC', 'AGNCL', 'AGNCM', 'AGNCN', 'AGNCO', 'AGNCP', 'AGO', 'AGR', 'AGRIW', 'AGRO', 'AGRX']

for symbol in [ticker for ticker in tickers if ticker not in done]:
  url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
  r = requests.get(url)
  dailyData = r.json()

  url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
  r = requests.get(url)
  companyData = r.json()

  if companyData.get('Symbol') and dailyData.get('Time Series (Daily)'):
    done.append(symbol)
    print(done)
    # Insert data into the company table
    print(f"Filling data for {companyData['Name']} ({companyData['Symbol']})")
    cursor.execute("""
        INSERT OR IGNORE INTO company (ticker, name, pe_ratio, dividend, earning_per_share, target_price, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (companyData['Symbol'], companyData['Name'], companyData['PERatio'], companyData['DividendYield'], companyData['EPS'], companyData['AnalystTargetPrice'], companyData['Description'])
    )
    dailyData = dailyData['Time Series (Daily)']
    for day in dailyData:
        # Insert data into the daily table
        cursor.execute("""
        INSERT INTO daily (ticker, date, price_open, price_closed)
        VALUES (?, ?, ?, ?)
        ON CONFLICT (ticker, date) DO NOTHING
        """,
        (companyData['Symbol'], day, dailyData[day]['1. open'], dailyData[day]['4. close'])
        )

    conn.commit()
    time.sleep(30)

  i += 1

  if i > 200:
    conn.close()
    exit()