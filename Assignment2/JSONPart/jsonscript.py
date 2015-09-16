import json
from haralyzer import HarParser, HarPage

with open('www.vox.com.har','r') as f:
	har_parser = HarParser(json.loads(f.read()))

print (har_parser.browser)

print har_parser.creator

