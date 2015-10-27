from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
import json
import os 
from wtforms import Form, BooleanField, StringField, validators

app = Flask(__name__)

app.config['SECRET_KEY'] = "ASECRET"

# Jinja
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
	return render_template('homepage.html')

@app.route('/get_rates', methods=['GET'])
def get_rates():
 	
 	rate_params = {}

 	# print rate_params
 	sample_rate_params = {
    "output": "json",
    "monthlydebts": "1500",
    "terminmonths": "360",
    "monthlypayment": "2000",
    "schedule": "yearly",
    "pmi": "1000",
    "debttoincome": "36.0",
    "hazard": "20000",
    "hoa": "10000",
    "callback": "cb",
    "propertytax": "20.0",
    "estimate": "false",
    "annualincome": "1000000",
    "incometax": "30.0",
    "zip": "91302",
    "down": "800000",
    "rate": "6.504"
}
	print sample_rate_params
	annualincome = request.args.get('annualincome', '')
	print annualincome
	rate_params['annualincome'] = int(annualincome)

	monthlypayment = request.args.get('monthlypayment', '')
	rate_params['monthlypayment'] = int(monthlypayment)

	down = request.args.get('down', '')
	rate_params['down'] = int(down)

	monthlydebts = request.args.get('monthlydebts', '')
	rate_params['monthlydebts'] = int(monthlydebts)

	rate = request.args.get('rate', '')
	rate_params['rate'] = int(rate)

	schedule = request.args.get('schedule', '')
	rate_params['schedule'] = str(schedule)

	term = request.args.get('term', '')
	rate_params['term'] = int(term)

	debttoincome = request.args.get('debttoincome', '')
	rate_params['debttoincome'] = int(debttoincome)

	incometax = request.args.get('incometax', '')
	rate_params['incometax'] = int(incometax)

	propertytax = request.args.get('propertytax', '')
	rate_params['propertytax'] = int(propertytax)

	hazardinsurance = request.args.get('hazardinsurance', '')
	rate_params['hazard'] = int(hazardinsurance)

	pmi = request.args.get('pmi', '')
	rate_params['pmi'] = int(pmi)

 	zipc = request.args.get('zipc', '')
	rate_params['zip'] = int(zipc)

 	estimate_yes = request.args.get('True', '')
 	# print estimate_yes
 	estimate_no = request.args.get('False', '')
	# print estimate_no
	if estimate_yes is False:
		rate_params['estimate'] = False
	if estimate_no is True:
		rate_params['estimate'] = True

	# print rate_params.values()
 	zwsid = 'X1-ZWz1eunt26vguj_6msnx'
	rate_params['zws-id'] = str(zwsid)

 	output = 'json'
	rate_params['output'] = output
	# print output
	# print rate_params

	rate_api_resp = requests.get('http://www.zillow.com/webservice/mortgage/CalculateAffordability.htm?', params=sample_rate_params)
	rate_info_api = rate_api_resp.json()
	print rate_info_api
	rate_info = rate_info_api['response']
	# print rate_info.keys()
	# print rate_info.values()

	# rate_info_lastWeek = rate_info_api["response"]["lastWeek"]
	# rate_info_today = rate_info_api['response']["today"]

	return render_template('rates.html', rate_info=rate_info)	
	
if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))

	app.debug = True

	DebugToolbarExtension(app)
	app.run(host='0.0.0.0', port=port)