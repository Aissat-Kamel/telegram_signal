import binance.client
from binance.client import Client
import pandas as pd
import numpy
import talib as ta
import Telegram_bot as Tb



Pkey = '' 
Skey = ''

client = Client(api_key=Pkey, api_secret=Skey)

intervals = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57]
connection = ""
ticker = "LTCUSDT"
period = 34


def indicator():
	rsi_stat = ""
	kline = client.get_historical_klines(ticker, "3m", "2 hours ago UTC+1")
	df = pd.DataFrame(kline)
	if not df.empty:
		df.columns = ['Date','Open','High','Low','Close' ,'Volume','IGNORE','Quote_Volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']
		df['Date'] =  pd.to_datetime(df['Date'],unit='ms')
		df = df.set_index('Date')
	rsi = ta.RSI(df["Close"], timeperiod = period)
	last_rsi = rsi[-2]
	if last_rsi < 30:
		rsi_stat = "RSI is Over sold"
	elif last_rsi > 70:
		rsi_stat = "RSI is Over bought"
	else :
		rsi_stat = "No signal"
	
	return round(last_rsi, 1), rsi_stat

def server_time():
	status = client.get_system_status()
	stat = status["status"]
	time_server = client.get_server_time()
	if stat == 0:
		connection = "Connected"
	else : 
		connection = "Disconnected"
	time = pd.to_datetime(time_server["serverTime"], unit="ms")
	minute = int(time.strftime("%M"))
	second = int(time.strftime("%S"))
	time_ = time.strftime("%H:%M:%S")
	nl = "%0D%0A"
	for i in intervals:
		if minute == i and second == 3:
			rsi = indicator()
			Tb.telegram_send_message("Time :"+time_+nl+"System state : "+connection+nl+"RSI now is : "+str(rsi[0])+nl+"RSI state : "+rsi[1])

		if minute == i+1 and second == 0:
			Tb.telegram_send_message("System is : "+ connection)
	

	



"""
while(True):
	server_time()

"""