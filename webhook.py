# Libraries required
import json 
import os
import requests

# Flask Library
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

# A decorator that tells Flask what URL should trigger 
# A decorator is a function which takes in a function and return a new function

@app.route('/webhook', methods=['POST'])
def webhook():
    # Extract the data which was sent in the JSON format 
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
return r 

# Extract the parameter from JSON , AJAX to openwaether , construct the respone according to it
def makeResponse(req):
    if req.get("result").get("action") != "fetchWeatherForecast":
    
    return {}
    # getting the json data in place
    result = req.get("result")
    parameters = result.get("parameters")
    # Here are the parameters getting in the JSOC , check the JSON output in API.AI
    city = parameters.get("geo-city")
    date = parameters.get("date")
    # query the API
    if city is None:
    return None
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=06f070197b1f60e55231f8c46658d077')
    # retireve
    json_object = r.json()
    weather=json_object['list']
    for i in range(0,30):
        if date in weather[i]['dt_txt']:
            condition= weather[i]['weather'][0]['description']
            break
    speech = "The forecast for"+city+ "for "+date+" is "+condition
    
    # returning the data back to the dialogflow , always check the fullfillment 
    return {
    "speech": speech,
    "displayText": speech,
    "source": "apiai-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















