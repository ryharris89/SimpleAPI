# This simple api was built as a sample api for the purposes of a job interview
# Built by: Ryan Harris

# Imports required for the api
from flask import Flask, request
from flask_restful import Api
from datetime import datetime
import pytz
import dateutil.parser
import json

# Initialize the api
app = Flask(__name__)
api = Api(app)

# Change this to the directory and file name of the JSON file to be used
JSONFile = "C:\\Users\\ryhar\\PycharmProjects\\flask_rest\\data.json"

# Starting page. Used to provide initial assistance for users
@app.route("/", methods=["GET"])
def home():
    return ("<h1>Parking Pricer API</h1><p>This API will assist with helping the user to determine the appropriate cost of parking when provided a start datetime and end datetime.</p><p>Click the following link to navigate to our pricing API: <a href='http://127.0.0.1:5000/api/v1/parking/pricer'>http://127.0.0.1:5000/api/v1/parking/pricer</a></p>"), 100

# api logic
@app.route("/api/v1/parking/pricer", methods=["GET"])
def api_id():
    # try opening the JSON file specified above
    try:
        with open(JSONFile, "r") as file:
            rates = json.loads(file.read())["rates"]
    # If file cannot be decoded by json package, alert the user
    except json.decoder.JSONDecodeError:
        helptext = ("<h1>Warning!</h1><p>JSON file is formatted or parsed incorrectly. Please fix this issue and restart the API engine.</p>")
        return helptext, 500
    # If directory/file provided above cannot be found, alert the user
    except FileNotFoundError:
        helptext = ("<h1>Warning!</h1><p>JSON file is missing or improperly linked. Please fix this issue and restart the API engine.</p>")
        return helptext, 500

    # try validating user api requests
    try:
        # If both api parameters are found, assign variables for start and end time
        if "StartDatetime" in request.args and "EndDatetime" in request.args:
            StartDatetime = list(request.args["StartDatetime"])
            StartDatetime[19] = StartDatetime[19].replace(" ", "+")
            StartDatetime = "".join(StartDatetime)
            EndDatetime = list(request.args["EndDatetime"])
            EndDatetime[19] = EndDatetime[19].replace(" ", "+")
            EndDatetime = "".join(EndDatetime)
        # If either api parameter is missing, alert the user
        if "StartDatetime" not in request.args or "EndDatetime" not in request.args:
            currentdatetime = (datetime.strptime(((dateutil.parser.parse(str(datetime.now(pytz.utc)))).isoformat()), "%Y-%m-%dT%H:%M:%S.%f%z")).strftime("%Y-%m-%d %H:%M:%S%z")
            helptext = ("<h1>Warning!</h1><p>Please include both StartDatetime and EndDatetime parameters with every request!</p><p>Also, make sure your datetimes are in the following format: yyyy-mm-dd hh:MM:ss+zzzz (Example: %s)</p>") % (currentdatetime,)
            return helptext, 400
        # If the dates provided are not the same, alert the user
        if str((datetime.strptime(request.args["StartDatetime"], "%Y-%m-%d %H:%M:%S%z")).strftime("%Y-%m-%d")) != str((datetime.strptime(request.args["EndDatetime"], "%Y-%m-%d %H:%M:%S%z")).strftime("%Y-%m-%d")):
            helptext = ("<h1>Warning!</h1><p>Please make sure your start time and end time fall on the same date!</p>")
            return helptext, 400
        # If datetimes provided are the exact same, alert the user
        if request.args["StartDatetime"] == request.args["EndDatetime"]:
            helptext = ("<h1>Warning!</h1><p>You cannot use the same exact values for the StartDatetime and EndDatetime.</p>")
            return helptext, 400
    # If the format of the datetimes is invalid, alert the user
    except ValueError:
        currentdatetime = (datetime.strptime(((dateutil.parser.parse(str(datetime.now(pytz.utc)))).isoformat()), "%Y-%m-%dT%H:%M:%S.%f%z")).strftime("%Y-%m-%d %H:%M:%S%z")
        helptext = ("<h1>Warning!</h1><p>The format of your datetime values is invalid.</p><p>Please make sure your datetimes are in the following format: yyyy-mm-dd hh:MM:ss+zzzz (Example: %s)</p>") % (currentdatetime,)
        return helptext, 400
    # If length of the datetimes was not long enough to form variables from above, alert the user
    except IndexError:
        currentdatetime = (datetime.strptime(((dateutil.parser.parse(str(datetime.now(pytz.utc)))).isoformat()), "%Y-%m-%dT%H:%M:%S.%f%z")).strftime("%Y-%m-%d %H:%M:%S%z")
        helptext = ("<h1>Warning!</h1><p>Please include both StartDatetime and EndDatetime parameters with every request!</p><p>Also, make sure your datetimes are in the following format: yyyy-mm-dd hh:MM:ss+zzzz (Example: %s)</p>") % (currentdatetime,)
        return helptext, 400

    # logic to determine the correct rate to provide the user
    for rate in rates:
        # Convert all input datetimes into timezone provided with rate within JSON file
        try:
            StartDatetime = (datetime.strptime(str(StartDatetime), "%Y-%m-%d %H:%M:%S%z")).astimezone(
                pytz.timezone(rate["tz"]))
            EndDatetime = (datetime.strptime(str(EndDatetime), "%Y-%m-%d %H:%M:%S%z")).astimezone(
                pytz.timezone(rate["tz"]))
        # If datetimes cannot be formatted into our local timezone, alert the user
        except ValueError:
            currentdatetime = (datetime.strptime(((dateutil.parser.parse(str(datetime.now(pytz.utc)))).isoformat()), "%Y-%m-%dT%H:%M:%S.%f%z")).strftime("%Y-%m-%d %H:%M:%S%z")
            helptext = ("<h1>Warning!</h1><p>The format of your datetime values is invalid.</p><p>Please make sure your datetimes are in the following format: yyyy-mm-dd hh:MM:ss+zzzz (Example: %s)</p>") % (currentdatetime,)
            return helptext, 400

        # Retrieve day from datetime and check if it is present in currently iterated rate
        if (StartDatetime.strftime("%a")).upper() in rate["days"].upper():
            # Check if start time and end time fall within the timeframe of the currently iterated rate. If so, provide the current rate
            if int(StartDatetime.strftime("%H%M")) >= int(rate["times"][:4]) and int(EndDatetime.strftime(("%H%M"))) <= int(rate["times"][5:]):
                return str(rate["price"]), 200
            # If the start time and end time do not fall within the same rate, alert the user
            else:
                helptext = ("<h1>Warning!</h1><p>The timeframe requested does not exist in the system.</p>")
                return helptext, 200
        # If day is not found in currently iterated rate, continue to next iteration of rate
        else:
            pass

    # If the day is not found in any of the iterated rates, alert user
    helptext = ("<h1>Warning!</h1><p>The day requested does not exist in the system.</p>")
    return helptext, 200

# Run the api engine
app.run(debug=False)