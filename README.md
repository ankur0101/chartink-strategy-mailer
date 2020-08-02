# Chartink Strategy mailer

A utility that sends an email alert about the stocks listed on Chartink strategy pages. You can trigger this automatically using linux cronjobs. I have integrated the given utility to work with AWS SES for mail sending which you can easily use with AWS Lambda, hence you are required to have AWS account. If not, you may tweak the code and add SMTP configuration.
## Installation

Python 3.6+ is required to run on your machine (Windows/Linux). Following commands will install dependencies 

```bash
pip3 install pyquery
pip3 install botocore
```

## Usage

```python
python run3.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU](https://choosealicense.com/licenses/gpl-3.0/)
