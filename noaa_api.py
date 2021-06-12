#! /usr/bin/env python

# noaa_api.py
# June 2021 by Zac Tobias
# 
# Retrieves 6-minute interval NOAA CO-OPs data across multiple months/years

Usage = "USAGE: noaa_api.py STATION START_DATE(YYYYMMDD) END_DATE(YYYYMMDD) PRODUCT, see https://api.tidesandcurrents.noaa.gov/api/prod/"

import sys
import datetime
import urllib.request

if (len(sys.argv) < 5) or (len(sys.argv) > 5):
	print("Must include station number, start date, end date, and product")
	print(Usage)
	exit()
else:
	station = str(sys.argv[1])
	start_date = str(sys.argv[2])
	end_date = str(sys.argv[3])
	product = str(sys.argv[4])

OutFileName = station+"_"+start_date+"_"+end_date+"_"+product+".csv"

OutFile = open(OutFileName, 'w')

start_date = datetime.date(int(start_date[0:4]), int(start_date[4:6].lstrip("0")), int(start_date[6:8].lstrip("0")))
end_date = datetime.date(int(end_date[0:4]), int(end_date[4:6].lstrip("0")), int(end_date[6:8].lstrip("0")))
delta_0 = datetime.timedelta(days=6)
delta_1 = datetime.timedelta(days=7)

print("Hacking the NOAA mainframe. Please wait.")

while start_date <= end_date:
	start_api = start_date.strftime("%Y%m%d")
	end_api = start_date + delta_0
	end_api = end_api.strftime("%Y%m%d")
	noaa_url="https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date="+start_api+"&end_date="+end_api+"&station="+station+"&product="+product+"&units=metric&time_zone=gmt&application=web_services&format=csv"
	response = urllib.request.urlopen(noaa_url)
	data = response.read().decode("utf-8")
	data = data.split("\n")
	for i, line in enumerate(data):
		if i==0 or i==1681:
			continue
		OutFile.write(line+"\n")
	start_date += delta_1

OutFile.close()

print("Your data file is ready! Share and enjoy.")
print(OutFileName)
