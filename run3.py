from lib import chartink
from lib import sendMail
#import boto3
#from botocore.exceptions import ClientError


timePeriod = ['[0] 1 hour', '[1] 1 hour', 'weekly', 'latest', '1 day ago', 'monthly']

jsonArray = []

for p in timePeriod:
	strategy1Json = chartink(
		'https://chartink.com/screener/strb',
		'scan_clause=(+%7B33619%7D+(+'+p+'+low+%3C%3D+'+p+'+supertrend(+10%2C2+)+and+'+p+'+open+%3E+'+p+'+supertrend(+10%2C2+)+and+'+p+'+close+%3E+'+p+'+supertrend(+10%2C2+)+and+'+p+'+high+%3E+'+p+'+supertrend(+10%2C2+)+)+)+'
	)
	for a in strategy1Json:
		a['timeframe'] = p
		jsonArray.append(a)
	


sendMail(jsonArray)
