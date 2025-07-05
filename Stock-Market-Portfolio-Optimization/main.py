#---------------collecting data on stocks-----------------
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

end_date = date.today().strftime('%Y-%m-%d')
start_date = (date.today() - timedelta(days=365)).strftime('%Y-%m-%d')

#list of banking stocks used for analysis 
tickers = ['HDFCBANK.NS' ,'ICICIBANK.NS','SBIN.NS','KOTAKBANK.NS' ,'AXISBANK.NS']

stock=yf.download(tickers,start=start_date,end=end_date,progress=False)
stock=stock.reset_index()
stock_melted  = stock.melt(id_vars=['Date'], var_name=['Attribute','Ticker'])
stock_pivoted  = stock_melted.pivot_table(index=['Date','Ticker'],columns='Attribute', values='value', aggfunc='first')

# reset index to turn multi-index into columns
stock_indexed = stock_pivoted.reset_index()
stock_indexed.head()

#-----------performance analysis over time--------------
import matplotlib.pyplot as plt
import seaborn as sns

stock_indexed['Date'] = pd.to_datetime(stock_indexed['Date'])
stock_indexed.set_index('Date',inplace=True)
stock_indexed.reset_index(inplace=True)
plt.figure(figsize=(10,5))

sns.lineplot(data=stock_indexed,x='Date',y='Adj Close',hue='Ticker', marker='*')

plt.title('STOCK PERFORMANCE')
plt.xlabel('Dates')
plt.ylabel('Adj closing')
plt.legend(title='Ticker')
plt.grid(True)

plt.show()


#50 days and 200 days moving avg
mavg=50 #moving avg 50
mavg1 = 200 #moving avg 200

stock_indexed.set_index('Date',inplace=True)
unique_tick = stock_indexed['Ticker'].unique()

#displaying Adj Close and moving avg of each stock
for ticker in unique_tick:
  ticker_date = stock_indexed[stock_indexed['Ticker']==ticker].copy()
  ticker_date['50_MA'] = ticker_date['Adj Close'].rolling(window=mavg).mean()
  ticker_date['200_MA'] = ticker_date['Adj Close'].rolling(window=mavg1).mean()

  plt.figure(figsize=(10,5))
  plt.plot(ticker_date.index, ticker_date['Adj Close'], label='Adjusting CLose price') 
  plt.plot(ticker_date.index, ticker_date['50_MA'], label='50 days moving avg')  
  plt.plot(ticker_date.index, ticker_date['200_MA'], label='200 days moving avg')

  plt.grid(True)
  plt.title(f'{ticker} Stock Adj close and Moving Avg graph')
  plt.legend()
  plt.xlabel('Date')
  plt.ylabel('Prices')

  plt.show()  


#----------------distribution of daily return of stocks-----------------

stock_indexed['Daily Return'] = stock_indexed.groupby('Ticker')['Adj Close'].pct_change()

plt.figure(figsize=(10,5))

for ticker in unique_tick:
    ticker_data=stock_indexed[stock_indexed['Ticker'] == ticker]
    sns.histplot(ticker_data['Daily Return'].dropna(), bins=50, kde=True, label=ticker, alpha=0.5)
    
plt.title('Distribution of Daily return')
plt.grid(True)
plt.xlabel('Daily Return')
plt.ylabel('Freq')
plt.legend()
plt.show()


#----------------generating expected returns-----------------
import numpy as np

daily_returns = stock_indexed.pivot_table(index='Date', columns='Ticker', values='Daily Return')
expected_return = daily_returns.mean() * 252
volatility = daily_returns.std() * np.sqrt(252)

new_data = pd.DataFrame({
    'Expected Return':expected_return,
    'Volatility': volatility
})

new_data


