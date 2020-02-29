from flask import Flask, request
import json
import sys
from flask import jsonify
from flask_cors import CORS, cross_origin
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

boundaries = None

with open('boundaries.json', 'r') as f:
    boundaries = json.load(f)

app = Flask(__name__)
# Allows for cross platform communication
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/greet')
def say_hello():
  return 'Hello from Server'

@app.route('/incoming_request', methods=['POST'])
def incoming_request():
    if request.method == 'POST':
        print(request.json, file=sys.stderr)
        # Here we print the data coming from the request
        # Running Tests
        benchmarking(boundaries, request.json)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        # Need to create a correct error message
        #error = 'Invalid username/password'
        return jsonify(success=False)


blood_data = {"patient": {"patientName": "Chiddy", "patientID": 1, "patientAge": 15, "patientGender": "male"}, "vitamins-and-minerals": {"Vitamin A": 8, "Vitamin B" : 3.51, "Vitamin C": 1.01}}



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

    print(patient_details)
    
    if int(patient_details["patientAge"]) < 18:
        person = "child"
    else:
        person = "adult"
        
    result = {"good":[], "bad":[]}
    
    for item in v_m:
        #3 three cases
        #case 1 the value is normal i.e. between lower and upper bound
        vit = {item: {"Explanation":"", "Side Effect": "", "Treatment": "", "Scores":{"value":0, "upper":0, "lower": 0, "average":0}, "Title":[], "Summary":[], "Link":[]}}
            
        item = item.replace(" ", "-")
        explanation, treatment, side_effects = call_api("conditions", "vitamins-and-minerals", item)
        
        treatment = BeautifulSoup(treatment, "lxml").text
        side_effects = BeautifulSoup(side_effects, "lxml").text
        explanation = BeautifulSoup(explanation, "lxml").text

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
    
    return json.dumps(result)

    
