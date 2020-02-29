# Testing out accessing an an API

# This script is using Python3
import urllib.request
import urllib.parse
import json

# Replace pageUrl with a page you want to call.

# key_word = "vitamin+c"
#
# pageURL = "https://api.nhs.uk/search/?query={}".format(key_word)
# # Replace {subscription-key} with your subscription key found here: https://developer.api.nhs.uk/developer.
# subscriptionKey = "37941d9c7f5449169a67cb5bc844e337"
#
# request_headers = {
#     "subscription-key": subscriptionKey,
#     "Accept": "application/json",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
# }
#
# request = urllib.request.Request(pageURL, headers=request_headers)
# contents = urllib.request.urlopen(request).read()
# json_contents = json.loads(contents)
#
# for content_module in json_contents:
#     print(content_module)
#
# print(contents[1])

# API type:
# Symptoms - access the conditions API using type, and syb type, and access the symptom list
# Treatments - access the conditions API and get the list of good sources of iron
# Medicine  - access the medicine API and see if you could could filter by sub-type somehow
# Side effects - Access the case where you take too much iron
#               - Side effects of the medicine you need to take



# url_dictionary = {
#     "symptoms":
# }


def call_api(api, condition_category_1, condition_category_2):


    subscriptionKey = "37941d9c7f5449169a67cb5bc844e337"

    request_headers = {
        "subscription-key": subscriptionKey,
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }

    if api == "conditions":

        pageURL = "https://api.nhs.uk/conditions/{}/{}".format(condition_category_1, condition_category_2)
        # Replace {subscription-key} with your subscription key found here: https://developer.api.nhs.uk/developer.
        request = urllib.request.Request(pageURL, headers=request_headers)
        contents = urllib.request.urlopen(request).read()
        json_contents = json.loads(contents)
        treatment = json_contents["mainEntityOfPage"][1]["mainEntityOfPage"][0]['text']
        side_effects = json_contents["mainEntityOfPage"][3]["mainEntityOfPage"][0]['text']

        return treatment, side_effects

    if api == "search":

        pageURL = "https://api.nhs.uk/search/?query={}".format(condition_category_2)
        request = urllib.request.Request(pageURL, headers=request_headers)
        contents = urllib.request.urlopen(request).read()
        json_contents = json.loads(contents)

        results = json_contents['results']

        results_of_search = []
        some_rando_dict = {}

        for idx, something in enumerate(results):
            some_rando_dict["title"] = results[idx]['title']
            some_rando_dict["summary"] = results[idx]['summary']
            some_rando_dict["url"] = results[idx]['url']
            results_of_search.append(some_rando_dict)

        print(results_of_search)

        return results_of_search


call_api("search","vitamins-and-minerals", "calcium")










