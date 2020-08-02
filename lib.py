#import sys
#sys.path.append('./packages')
import requests
from pyquery import PyQuery as pq
import json
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

def sendMail(strategy1Json):
	now = datetime.now()
	date = now.strftime("%d %B, %Y")
	SENDER = "Senders Name<sender@email.tld>"
	RECIPIENT = "receiver@emai.tld"

	#CONFIGURATION_SET = "ConfigSet"

	# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
	AWS_REGION = "us-east-1"

	# The subject line for the email.
	SUBJECT = "SuperTrend report for "+date

	# The email body for recipients with non-HTML email clients.
	BODY_TEXT = ("SuperTrend report for "+date)

	BODY_HTML = """<p>Hello <Receiver>,</p>
		<p>Please find the reports below for """+ date +"""</p>
		<table class="editorDemoTable">
		<tbody>
		<tr>
		<td><strong>Stock Name</strong></td>
		<td><strong>Interval</strong></td>
		</tr>
		"""
	for m in strategy1Json:
		BODY_HTML = BODY_HTML + """
		<tr>
		<td>"""+ m['nsecode'] +"""</td>
		<td>"""+ m['timeframe'] +"""</td>
		</tr>
		"""
		
	BODY_HTML = BODY_HTML + """
		</tbody>
		</table>
		<p>Thanks</p>
				"""            

	# The character encoding for the email.
	CHARSET = "UTF-8"

	# Create a new SES resource and specify a region.
	client = boto3.client('ses',region_name=AWS_REGION)

	# Try to send the email.
	try:
		#Provide the contents of the email.
		response = client.send_email(
			Destination={
				'ToAddresses': [
					RECIPIENT,
				],
			},
			Message={
				'Body': {
					'Html': {
						'Charset': CHARSET,
						'Data': BODY_HTML,
					},
					'Text': {
						'Charset': CHARSET,
						'Data': BODY_TEXT,
					},
				},
				'Subject': {
					'Charset': CHARSET,
					'Data': SUBJECT,
				},
			},
			Source=SENDER,
			# If you are not using a configuration set, comment or delete the
			# following line
			#ConfigurationSetName=CONFIGURATION_SET,
		)
	# Display an error if something goes wrong.	
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		print("Email sent! Message ID:"),
		print(response['MessageId'])


def chartink(url, payload):
	headers = {
	  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
	  'Cookie': 'XSRF-TOKEN=eyJpdiI6IndCTWpRSXVQTmRtdFlmejZYcTUzdHc9PSIsInZhbHVlIjoiNHg3TTVqRG05RDI2ZGh2V0ZcL2VsaWVlYVVOdlpcLzJVQXI4OFY1WjBnNU13alUyRUJ5cFk5YjNvWTNUK0puV3piIiwibWFjIjoiOTU0MjQzOTczMDQ2ZGUzOTJiMDViYjk1NjU5NGZmYzVlYzc5OWYzMTBjODg3ZTcwOTZiNDRjY2IxNWUzMmMyMiJ9; ci_session=eyJpdiI6ImFUY0tRUWxxNlVpVTZhYzVKc3VZa0E9PSIsInZhbHVlIjoiZXhsbzdiMW00ekVhUVBPM1o3S1Y3UFFlQlc3ZTh0QWRmeUpyWUxaYzR0WitaM0plOHV4Z1lOYVBpNWFPYnU1YyIsIm1hYyI6ImQ4YzIwY2ZlYzM3YjZmZGY0OWM0ZTI0YmZjMWQ1MmUxNTVmZjAxM2I1MTc2NWExMzljMDAwZjA0NTkzNWE3NTAifQ%3D%3D'
	}
	cookies = {}

	response = requests.request("GET", url)

	html = pq(response.text.encode('utf8'))
	csrf_token = html('meta[name="csrf-token"]').attr('content')

	cookies['XSRF-TOKEN'] = response.cookies['XSRF-TOKEN']
	cookies['ci_session'] = response.cookies['ci_session']
	
	#Preparing request
	newurl = "https://chartink.com/screener/process"

	#'scan_clause=%28%20%7B33619%7D%20%28%20weekly%20low%20%3C%3D%20weekly%20lower%20bollinger%20band%28%2010%2C2%20%29%20%29%20%29%20'
	#payload = 'scan_clause=(+%7B57960%7D+(+%5B0%5D+15+minute+close+%3E+%5B-1%5D+15+minute+max(+20+%2C+%5B0%5D+15+minute+close+)+and+%5B0%5D+15+minute+volume+%3E+%5B0%5D+15+minute+sma(+volume%2C20+)+)+)+'

	newheaders = {
	  'Accept': 'application/json, text/javascript, */*; q=0.01',
	  'Accept-Encoding': 'gzip, deflate, br',
	  'Accept-Language': 'en-US,en;q=0.5',
	  'Connection': 'keep-alive',
	  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	  #'Cookie': 'XSRF-TOKEN=eyJpdiI6InhhNEd0RHpBc2lCMFZXdDdcL1JoYWZnPT0iLCJ2YWx1ZSI6InNoV0NnanlJbEtuV012bkNtRE9rQ01uRGY2ek5lcWVCRUpkTDRiN1hPSkIxYzRUT2xmV0prYjlBZmtYaG1LcVUiLCJtYWMiOiIyZWMyZjIzZWI2YjkwNmMxZTQ2ZWI1OTQ4OTI3ZDU3ZWUyZWZjZjJjMDkxMGVjZTYwZTAxYjRkNTJiODM0YzA4In0%3D;ci_session=eyJpdiI6IndicENpS2ZXVGZrS1NKeUFBK3AzOXc9PSIsInZhbHVlIjoiaEZ3Z3Zva2JFK2lMWFJpaWliaEh4SnhlUDhEMHptT0l0bXQ1Kys5U3N2ZTU0anZNQTZsbFwvSmlyY2N0SVwvc0xyIiwibWFjIjoiMzc1NmJiMjg2MjczMGQ4MzRmNzNmNDM4ZGExODMxY2FhNjM2OGYxZDcyZjA2NTYwZDJkNTJiNTk5YjRmZDBjNyJ9; XSRF-TOKEN=eyJpdiI6InlqZmpUOG5qUVZVUFdcLzRKamRmaHZ3PT0iLCJ2YWx1ZSI6IjNRN3JxWFFOcVU1eEU0Z2hJd3hBYWtzSUFSU1Z6WXgyYmpwK0R2Mm9BeHNEMDdIYW40ZnpYR2MwbVVrN0pRNVAiLCJtYWMiOiI0OGVkZWEzMTk2ZjIzODRkNGM1MWIyOGQxMGM1ZjExZjQxZGJiNGQzZTkxN2Y3NDA4NDc3MWFjMTFhZjIzNjBhIn0%3D; ci_session=eyJpdiI6ImRtdVNlSGRPcWk4OG51a1dTdWgwMUE9PSIsInZhbHVlIjoiQ1wvazJtU3JNbXhweHRORzE1bGlJdTIwWFZ5dVZINXYxMnNCeW9aVFB4ZEJzTG9oenBScDBkNldLWWxHMndFXC9WIiwibWFjIjoiZDMwNDFlMmEyM2I5Yjg5OTQ5YTZjOGYwNWY1NGU3ZTY1YTJlNzVmZTc1NGUyZTc3ZTY1MDU4NzI5MGExMDdhNiJ9',
	  'Host': 'chartink.com',
	  'Referer': url, #'https://chartink.com/screener/15-minute-stock-breakouts',
	  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
	  #'X-CSRF-TOKEN': 'xN9K9eVKND6wleBWz3jPuO68HBFOYurYVenK4zOe',
	  'X-Requested-With': 'XMLHttpRequest',
	  'origin': 'https://chartink.com',
	  'referer': url, #'https://chartink.com/screener/15-minute-stock-breakouts',
	  'sec-fetch-dest': 'empty',
	  'sec-fetch-mode': 'cors',
	  'sec-fetch-site': 'same-origin'
	}
	newheaders['X-CSRF-TOKEN'] = csrf_token
	newheaders['Cookie'] = 'XSRF-TOKEN='+cookies['XSRF-TOKEN']+';ci_session='+cookies['ci_session']
	newresponse = requests.request("POST", newurl, headers=newheaders, data = payload)
	jsonoutput = json.loads( newresponse.text.encode('utf8') )
	return jsonoutput['data']
