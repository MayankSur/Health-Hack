from flask import Flask, redirect, url_for, render_template, request, session, flash
import json
import sys
from flask import jsonify
from flask_cors import CORS, cross_origin
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from unidecode import unidecode
import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

boundaries = None

with open('boundaries.json', 'r') as f:
    boundaries = json.load(f)

local_updates = None
graph = None

app = Flask(__name__)
# Allows for cross platform communication
cors = CORS(app, resources={r"/*": {"origins": "*"}})
  
def create_plot():


    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/greet')
def say_hello():
  return 'Hello from Server'

@app.route('/incoming_request', methods=['POST'])
def incoming_request():
	if request.method == 'POST':
		print(request.json, file=sys.stderr)
		# Here we print the data coming from the request
		# Running Tests
		output = benchmarking(boundaries, request.json)
		
		global local_updates
		local_updates = output.decode()
		local_updates = json.loads(local_updates)
		print(local_updates["good"])
		LB = local_updates["good"][0]['Vitamin A']["Scores"]["lower"]
		UB = local_updates["good"][0]['Vitamin A']["Scores"]["upper"]
		user_value = local_updates["good"][0]['Vitamin A']["Scores"]["value"]
		trace1 = go.Box(x=list(range(int(LB - (UB-LB)/2), int(UB + (UB-LB)/2))), name="Vitamin A", fillcolor="crimson", marker=dict(size=12,line=dict(width=2,color='DarkSlateGrey')))
		data = [trace1]
		graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
		# print(graphJSON)
		global graph
		graph = graphJSON
		return render_template('tests.html', values=local_updates, graphJSON=graph, dick='HELLO')
	else:
		# Need to create a correct error message
		#error = 'Invalid username/password'
		return jsonify(success=False)

# @app.route('/test', methods=['GET'])
# def test():
# 	return render_template('tests.html', values={"Hello World!": 'CHIDS'})

#blood_data = {"patient": {"patientName": "Chiddy", "patientID": 1, "patientAge": 15, "patientGender": "male"}, "vitamins-and-minerals": {"Vitamin A": 8, "Vitamin B" : 3.51, "Vitamin C": 1.01}}



def call_api(api, condition_category_1, condition_category_2):


    subscriptionKey = "37941d9c7f5449169a67cb5bc844e337"

    request_headers = {
        "subscription-key": subscriptionKey,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }

    if api == "conditions":

        pageURL = "https://api.nhs.uk/conditions/{}/{}".format(condition_category_1, condition_category_2)
#        print("PAGE",pageURL)
        # Replace {subscription-key} with your subscription key found here: https://developer.api.nhs.uk/developer.
        request = urllib.request.Request(pageURL, headers=request_headers)
        contents = urllib.request.urlopen(request).read()
        json_contents = json.loads(contents)
#        print(json_contents)
        treatment = json_contents["mainEntityOfPage"][1]["mainEntityOfPage"][0]['text']
        side_effects = json_contents["mainEntityOfPage"][3]["mainEntityOfPage"][0]['text']
        explanation = json_contents["mainEntityOfPage"][0]["mainEntityOfPage"][0]['text']
        
        return explanation, treatment, side_effects

    if api == "search":
        
        pageURL = "https://api.nhs.uk/search/?query={}".format(condition_category_2)
#        print("PAGE",pageURL)
        request = urllib.request.Request(pageURL, headers=request_headers)
        contents = urllib.request.urlopen(request).read()
        json_contents = json.loads(contents)

        results = json_contents['results']

        results_of_search = []
        

        for idx, something in enumerate(results):
            some_rando_dict = {}
            some_rando_dict["title"] = results[idx]['title']
            some_rando_dict["summary"] = results[idx]['summary']
            some_rando_dict["url"] = results[idx]['url']
            results_of_search.append(some_rando_dict)

        return results_of_search

        
def benchmarking(lut, data):
    v_m = data["vitamins-and-minerals"]
    patient_details = data["patient"]

    # print(patient_details)
    
    if int(patient_details["patientAge"]) < 18:
        person = "child"
    else:
        person = "adult"
        
    result = {"ppi": patient_details ,"good":[], "bad":[]}
    
    for item in v_m:
        #3 three cases
        #case 1 the value is normal i.e. between lower and upper bound
        vit = {item: {"Explanation":"", "Side Effect": "", "Treatment": "", "Scores":{"value":0, "upper":0, "lower": 0, "average":0}, "Title":[], "Summary":[], "Link":[]}}
            
        item = item.replace(" ", "-")
        explanation, treatment, side_effects = call_api("conditions", "vitamins-and-minerals", item)
        
        treatment = BeautifulSoup(treatment, "lxml").text.replace("\n", " ")
        side_effects = BeautifulSoup(side_effects, "lxml").text.replace("\n", " ")
        explanation = BeautifulSoup(explanation, "lxml").text.replace("\n", " ")

        item = item.replace("-", " ")
        
        vit[item]["Scores"]["value"] = float(v_m[item])
        vit[item]["Scores"]["lower"] = boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["lower"]
        vit[item]["Scores"]["upper"] = boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["upper"]
        vit[item]["Scores"]["average"] = boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["average"]
        
        if boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["lower"] <= float(v_m[item]) <= boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["upper"]:
            vit[item]["Explanation"] = explanation
            result["good"].append(vit)
        
        #case 2, 3 the value is abnormal i.e. less than lower or higher than upper
        if boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["lower"] >= float(v_m[item]) or float(v_m[item]) >= boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["upper"]:
            vit[item]["Explanation"] = explanation
            item = item.replace(" ", "+")
            output = call_api("search", "vitamins-and-minerals", item)
            item = item.replace("+", " ")
            vit[item]["Side Effect"] = side_effects
            vit[item]["Treatment"] = treatment
            for i in output:
                vit[item]["Title"].append(i["title"])
                vit[item]["Summary"].append(i["summary"])
                vit[item]["Link"].append(i["url"])
            
            result["bad"].append(vit)
    
    return json.dumps(result, ensure_ascii=False).encode('utf8')

app = Flask(__name__)
# Allows for cross platform communication
cors = CORS(app, resources={r"/*": {"origins": "*"}})
  
def create_plot():


    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/greet')
def say_hello():
  return 'Hello from Server'

@app.route('/incoming_request', methods=['POST'])
def incoming_request():
	if request.method == 'POST':
		print(request.json, file=sys.stderr)
		# Here we print the data coming from the request
		# Running Tests
		output = benchmarking(boundaries, request.json)
		
		global local_updates
		local_updates = output.decode()
		local_updates = json.loads(local_updates)
		print(local_updates["good"])
		LB = local_updates["good"][0]['Vitamin A']["Scores"]["lower"]
		UB = local_updates["good"][0]['Vitamin A']["Scores"]["upper"]
		user_value = local_updates["good"][0]['Vitamin A']["Scores"]["value"]
		trace1 = go.Box(x=list(range(int(LB - (UB-LB)/2), int(UB + (UB-LB)/2))), name="Vitamin A", fillcolor="crimson", marker=dict(size=12,line=dict(width=2,color='DarkSlateGrey')))
		data = [trace1]
		graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
		# print(graphJSON)
		global graph
		graph = graphJSON
		return render_template('tests.html', values=local_updates, graphJSON=graph, dick='HELLO')
	else:
		# Need to create a correct error message
		#error = 'Invalid username/password'
		return jsonify(success=False)

# @app.route('/test', methods=['GET'])
# def test():
# 	return render_template('tests.html', values={"Hello World!": 'CHIDS'})

#blood_data = {"patient": {"patientName": "Chiddy", "patientID": 1, "patientAge": 15, "patientGender": "male"}, "vitamins-and-minerals": {"Vitamin A": 8, "Vitamin B" : 3.51, "Vitamin C": 1.01}}



def call_api(api, condition_category_1, condition_category_2):


    subscriptionKey = "37941d9c7f5449169a67cb5bc844e337"

    request_headers = {
        "subscription-key": subscriptionKey,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }

    if api == "conditions":

        pageURL = "https://api.nhs.uk/conditions/{}/{}".format(condition_category_1, condition_category_2)
#        print("PAGE",pageURL)
        # Replace {subscription-key} with your subscription key found here: https://developer.api.nhs.uk/developer.
        request = urllib.request.Request(pageURL, headers=request_headers)
        contents = urllib.request.urlopen(request).read()
        json_contents = json.loads(contents)
#        print(json_contents)
        treatment = json_contents["mainEntityOfPage"][1]["mainEntityOfPage"][0]['text']
        side_effects = json_contents["mainEntityOfPage"][3]["mainEntityOfPage"][0]['text']
        explanation = json_contents["mainEntityOfPage"][0]["mainEntityOfPage"][0]['text']
        
        return explanation, treatment, side_effects

    if api == "search":
        
        pageURL = "https://api.nhs.uk/search/?query={}".format(condition_category_2)
#        print("PAGE",pageURL)
        request = urllib.request.Request(pageURL, headers=request_headers)
        contents = urllib.request.urlopen(request).read()
        json_contents = json.loads(contents)

        results = json_contents['results']

        results_of_search = []
        

        for idx, something in enumerate(results):
            some_rando_dict = {}
            some_rando_dict["title"] = results[idx]['title']
            some_rando_dict["summary"] = results[idx]['summary']
            some_rando_dict["url"] = results[idx]['url']
            results_of_search.append(some_rando_dict)

        return results_of_search

        
def benchmarking(lut, data):
    v_m = data["vitamins-and-minerals"]
    patient_details = data["patient"]

    # print(patient_details)
    
    if int(patient_details["patientAge"]) < 18:
        person = "child"
    else:
        person = "adult"
        
    result = {"ppi": patient_details ,"good":[], "bad":[]}
    
    for item in v_m:
        #3 three cases
        #case 1 the value is normal i.e. between lower and upper bound
        vit = {item: {"Explanation":"", "Side Effect": "", "Treatment": "", "Scores":{"value":0, "upper":0, "lower": 0, "average":0}, "Title":[], "Summary":[], "Link":[]}}
            
        item = item.replace(" ", "-")
        explanation, treatment, side_effects = call_api("conditions", "vitamins-and-minerals", item)
        
        treatment = BeautifulSoup(treatment, "lxml").text.replace("\n", " ")
        side_effects = BeautifulSoup(side_effects, "lxml").text.replace("\n", " ")
        explanation = BeautifulSoup(explanation, "lxml").text.replace("\n", " ")

        item = item.replace("-", " ")
        
        vit[item]["Scores"]["value"] = float(v_m[item])
        vit[item]["Scores"]["lower"] = boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["lower"]
        vit[item]["Scores"]["upper"] = boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["upper"]
        vit[item]["Scores"]["average"] = boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["average"]
        
        if boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["lower"] <= float(v_m[item]) <= boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["upper"]:
            vit[item]["Explanation"] = explanation
            result["good"].append(vit)
        
        #case 2, 3 the value is abnormal i.e. less than lower or higher than upper
        if boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["lower"] >= float(v_m[item]) or float(v_m[item]) >= boundaries["vitamins-and-minerals"][item][person][patient_details["patientGender"]]["upper"]:
            vit[item]["Explanation"] = explanation
            item = item.replace(" ", "+")
            output = call_api("search", "vitamins-and-minerals", item)
            item = item.replace("+", " ")
            vit[item]["Side Effect"] = side_effects
            vit[item]["Treatment"] = treatment
            for i in output:
                vit[item]["Title"].append(i["title"])
                vit[item]["Summary"].append(i["summary"])
                vit[item]["Link"].append(i["url"])
            
            result["bad"].append(vit)
    
    return json.dumps(result, ensure_ascii=False).encode('utf8')

    

app.secret_key ="ICHACK_2020"

user_names=["Ivan"]
user_password=["test"]

@app.route("/")
def home():
	return render_template("login1.html")

@app.route("/login",methods=["POST","GET"])
def login():
	if request.method=="POST":
		user_test = request.form["nm"]
		password_test = request.form["ps"]
		if user_test==user_names[0] and password_test==user_password[0]:
			session["user"] = user_test
			return render_template("general.html",user=user_test)
		else:
			flash("Wrong username or password! Try again!")
			return render_template("login1.html")
	else:
		if "user" in session:
			flash("Already logged in")
			return redirect(url_for("user"))
		return render_template("login1.html")

@app.route("/general")
def general():
	user=session["user"]
	return render_template("general.html",user=user)

@app.route("/info")
def info():
	user=session["user"]
	return render_template("info.html",user=user)

@app.route("/tests")
def tests():
	user=session["user"]
	global local_updates  
	global graph
	return render_template("tests.html",user=user, values=local_updates, graphJSON=graph)

@app.route("/history")
def history():
	user=session["user"]
	return render_template("history.html",user=user)

@app.route("/settings")
def settings():
	user=session["user"]
	return render_template("settings.html",user=user)

@app.route("/logout")
def logout():
	session.pop("user",None)
	return render_template("login1.html")


if __name__=="__main__":
     app.run(debug=True)

