#Title: Scanner.py
#Authors: Wanderer and Bohdi
#Date: 02/29/2021
#Purpose:	
# Provide a basic scanner that accepts a ticker input
# and returns the following:
#	- previous close 
# 	- previous open
# 	- days range
# 	- 52 week range
# 	- volume
# 	- avg volume
# 	- mkt cap
# 	- 5y monthly beta
# 	- next earnings date

#import modules
import pandas as pd

class Scanner:
	#Variables:
	#Ticker input
	company = 'AAPL'
	#URL to pull data from
	dataSource = f'https://finance.yahoo.com/quote/{company}/key-statistics?p={company}'
	#read_html from selected dataSource URL using Pandas
	df = pd.read_html(dataSource)
	
	#Data frames separated
	valuationMeasures = df[0]
	stockPriceHistory = df[1]
	shareStatistics = df[2]
	dividendInfo = df[3]
	profitabilityInfo = df[5]
	managementEfectiveness = df[6]
	incomeStatement = df[7]
	balanceSheet = df[8]
	cashFlow = df[9]

	#Individual output selections
	FiftyDMovAvg = stockPriceHistory.filter(like = '5', axis=0)

	print(FiftyDMovAvg)
	#Export results to excel
	valuationMeasures.to_excel('test.xlsx')

#End of Scanner class