from flask import Flask, request
import json
import sys
from flask import jsonify
from flask_cors import CORS, cross_origin
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup


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
        print("PAGE",pageURL)
        # Replace {subscription-key} with your subscription key found here: https://developer.api.nhs.uk/developer.
        request = urllib.request.Request(pageURL, headers=request_headers)
        contents = urllib.request.urlopen(request).read()
        json_contents = json.loads(contents)
        print(json_contents)
        treatment = json_contents["mainEntityOfPage"][1]["mainEntityOfPage"][0]['text']
        side_effects = json_contents["mainEntityOfPage"][3]["mainEntityOfPage"][0]['text']

        return treatment, side_effects

    if api == "search":
        
        pageURL = "https://api.nhs.uk/search/?query={}".format(condition_category_2)
        print("PAGE",pageURL)
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

#        print(results_of_search)

        return results_of_search


#call_api("search","vitamins-and-minerals", "calcium")

        
def benchmarking(lut, data):
    v_m = data["vitamins-and-minerals"]
    patient_details = data["patient"]
    
    if patient_details["age"] < 18:
        person = "child"
    else:
        person = "adult"
    
    for item in v_m:
        #3 three cases
        #case 1 the value is normal i.e. between lower and upper bound
        if boundaries["vitamins-and-minerals"][item][person][patient_details["gender"]]["lower"] <= v_m[item] <= boundaries["vitamins-and-minerals"][item][person][patient_details["gender"]]["upper"]:
            print("Normal")
        #case 2, 3 the value is abnormal i.e. less than lower or higher than upper
        if boundaries["vitamins-and-minerals"][item][person][patient_details["gender"]]["lower"] >= v_m[item] or v_m[item] >= boundaries["vitamins-and-minerals"][item][person][patient_details["gender"]]["upper"]:
            item = item.replace(" ", "+")
            output = call_api("search", "vitamins-and-minerals", item)
#            for v in output:
#                print("title:", v["title"])
#                print("summary:", v["summary"])
#                print("url:", v["url"])
                
            item = item.replace("+", "-")
            treatment, side_effects = call_api("conditions", "vitamins-and-minerals", item)
            
            # Parse the html content
            soup = BeautifulSoup(treatment, "lxml")
#            print(soup.prettify()) 
            print(soup.text)
            
            soup_effects = BeautifulSoup(side_effects, "lxml")
#            print(soup_effects.prettify()) 
            print(soup_effects.text)
    
    return "Done"

benchmarking(boundaries, blood_data)
    

#request_headers = {
#  "subscription-key": subscriptionKey,
#  "Accept": "application/json",
#  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
#}
# 
#request = urllib.request.Request(pageURL, headers=request_headers)
#contents = urllib.request.urlopen(request).read()
#parsed_content = json.loads(contents)

