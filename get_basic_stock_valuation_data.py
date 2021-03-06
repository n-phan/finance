import csv
import json
import re
from wsgiref import headers
import requests
from bs4 import BeautifulSoup

request_headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } 

csv_header = ['Ticker', 'Beta (5Y Monthly)', 'Payout Ratio', 'Dividend', 'Return on Equity (ttm)']
tickers = ['AMAT', 'INTC', 'AMD']


def get_json_data(url):
    response = requests.get(url, headers=request_headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r'\s--\sData\s--\s')
    script_data = soup.find('script', text=pattern).contents[0]
    start = script_data.find("context")-2
    return json.loads(script_data[start:-12])




with open('dump.csv', 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(csv_header)

    for ticker in tickers:
        url = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'.format(ticker, ticker)
        json_data = get_json_data(url)
        summary_data = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']

        beta = summary_data['beta']['raw']
        payout_ratio = summary_data['payoutRatio']['raw']
        dividend = summary_data['dividendRate']['raw'] if ('raw' in summary_data['dividendRate'].keys()) else 0.00
        return_on_equity = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['financialData']['returnOnEquity']['raw']

        data = [ticker, beta, payout_ratio, dividend, return_on_equity]

        filewriter.writerow(data)
