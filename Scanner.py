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
#import modules
from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd

class Scanner:
	# Set up the request headers that we're going to use, to simulate
	# a request by the Chrome browser. Simulating a request from a browser
	# is generally good practice when building a scraper
	def getPage(self, url):
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.9',
			'Cache-Control': 'max-age=0',
			'Pragma': 'no-cache',
			'Referrer': 'https://google.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
		}

		return requests.get(url, headers=headers)

	#Parse rows
	def parseRows(self, tableRows):
		parsedRows = []

		for tableRow in tableRows:
			parsedRow = []
			el = tableRow.xpath("./div")

			noneCount = 0

			for rs in el:
				try:
					(text,) = rs.xpath('.//span/text()[1]')
					parsedRow.append(text)
				except ValueError:
					parsedRow.append(np.NaN)
					noneCount += 1

			if (noneCount < 4):
				parsedRows.append(parsedRow)
				
		return pd.DataFrame(parsedRows)

	#Individual row output selections
	def findItem(self, dataFrame, item, column):
		#selectOutput var = dataframe.locate[df column name] and row equals grossProfit var
		selectOutput = dataFrame.loc[dataFrame[column] == item]

		return selectOutput
	
	#Scrape specified table
	def scrapeTable(self, url):
		# Fetch the page that we're going to parse
		page = self.getPage(url)

		# Parse the page with LXML, so that we can start doing some XPATH queries
		# to extract the data that we want
		tree = html.fromstring(page.content)

		# Fetch all div elements which have class 'D(tbr)'
		tableRows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
		
		# Ensure that some table rows are found; if none are found, then it's possible
		# that Yahoo Finance has changed their page layout, or have detected
		# that you're scraping the page.
		assert len(tableRows) > 0
		
		df = self.parseRows(tableRows)
		#Make row 0 the column names when displayed/queried
		df.columns = df.iloc[0]

		#return output
		return df
#End of Scanner class

if __name__ == "__main__":
	#Scanner class run as var
	scannerObj = Scanner()
	#Symbol
	symbol = 'AAPL'
	#Output findItem(scrapeTable - gets df, item to find, column item is found in)
	print(scannerObj.findItem(scannerObj.scrapeTable('https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol), 'Gross Profit', 'Breakdown'))