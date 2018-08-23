import pandas_datareader.data as web
import datetime

start_year = 2014
end_year = 2017

output_file = "orcl-"+str(start_year)+"-"+str(end_year)+".csv"

start = datetime.datetime(start_year, 1, 1)
end = datetime.datetime(end_year, 12, 31)
company = "ORCL"
data = web.DataReader(company, 'iex', start, end)

data.to_csv(output_file, encoding="utf-8", sep=",")