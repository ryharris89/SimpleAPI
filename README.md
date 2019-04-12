# SimpleAPI
This simple API was built for the purposes of a job interview.

Tested with Python 3.7.

In order to run this python script, you will need to ensure the following python packages are installed via pip:
flask, flask_restful, pytz, dateutil.parser, datetime, and json

Before running this API script, it is important to change the JSONFile variable to the location of your JSON file of choice (or you may download the data file in this repository and use it instead).

This API essentially takes a provided JSON file as the backend data source. Users may interact with this API locally (http://127.0.0.1:5000/) on their machines once the script has been executed.

This API contains one endpoint: http://127.0.0.1:5000/api/v1/parking/pricer
To communicate with this endpoint, you must use the following parameters: StartDatetime, EndDatetime.
The datetimes provided to this endpoint must be in ISO-8601 format and include timezones (Example: 2019-03-25 02:17:46-0500).

If you run into any issues when testing this API, see the on-screen error handling to assist you with the most likely cause of the issue.
