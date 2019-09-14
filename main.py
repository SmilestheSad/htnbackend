#!python3
from flask import Flask
import urllib.request
import json
app = Flask(__name__)

# foodname -> string
# blacklist -> comma seperated list of strings e.g. "apple,banna,orange"

APP_ID = "08c67c26"
APP_KEY = "d22fafacab5449e1405a9937b7a0a7ba"

@app.route('/<foodname>/<blacklist>')
def f(foodname, blacklist):
    for x in blacklist:  # parse blacklist
        x = x.lower()
    foodname = foodname.replace(" ", "%20")  # parse foodname

    # Request list of ingredients for dish from Edamam API
    # change amount of results later maybe if need more precision
    url = "https://api.edamam.com/search?q="+foodname+"&app_id="+APP_ID+"&app_key=" + APP_KEY + "&to=100"
    print(url)
    contents = urllib.request.urlopen(url).read()
    ingredients = []
    contents = json.loads(contents)
    
    hits = contents["hits"]  # list of recipes

    # look through recipes and their ingredients
    for hit in hits:
        recipe = hit["recipe"]
        ingred = recipe["ingredients"]



        # print(ingred)
        for x in ingred:
            # print(x["text"])
            ingredients.append(x["text"])

    bad = blacklist.split(",")

    # count appearances of blacklisted ingredients in recipes
    cnt = {}
    test = []
    res = dict()
    conf = dict()
    for i in bad:
        a = 0
        for j in ingredients:
            a += j.lower().count(i)
        
        cnt[i] = a
        print("count of "+i+" is "+str(a))
        test.append("count of "+i+" is "+str(a))

        res[i] = a/100  # % chance that a blacklisted ingredient will be in dish given recipes (NOT VERY ACCURATE)

        # Give user confidence level
        if res[i] <= 0.1:
            conf[i] = "Very Unlikely"
        elif res[i] <= 0.3:
            conf[i] = "Unlikely"
        elif res[i] <= 0.6:
            conf[i] = "Moderate Chance"
        elif res[i] <= 0.8:
            conf[i] = "Likely"
        else:
            conf[i] = "Very Likely"

    # print(contents)
    return str(conf)

if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port = 42068, debug = True)