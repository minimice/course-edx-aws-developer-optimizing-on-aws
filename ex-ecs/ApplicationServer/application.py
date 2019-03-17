# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except
# in compliance with the License. A copy of the License is located at
#
# https://aws.amazon.com/apache-2-0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"Application server for timezones app"
import os
from datetime import datetime
import pytz
from flask import Flask, jsonify

application = Flask(__name__)

ZONES = {
    'us-east-1' : {'Title' : 'N. Virginia', 'TZ' : 'US/Eastern'},
    'us-east-2' : {'Title' : 'Ohio', 'TZ' : 'US/Eastern'},
    'us-west-1' : {'Title' : 'N. California', 'TZ' : 'US/Pacific'},
    'us-west-2' : {'Title' : 'Oregon', 'TZ' : 'US/Pacific'},
    'ap-south-1' : {'Title' : 'Mumbai', 'TZ' : 'Asia/Kolkata'},
    'ap-northeast-2' : {'Title' : 'Seoul', 'TZ' : 'Asia/Seoul'},
    'ap-southeast-1' : {'Title' : 'Singapore', 'TZ' : 'Asia/Singapore'},
    'ap-southeast-2' : {'Title' : 'Sydney', 'TZ' : 'Australia/Sydney'},
    'ap-northeast-1' : {'Title' : 'Tokyo', 'TZ' : 'Asia/Tokyo'},
    'ca-central-1' : {'Title' : 'Montreal', 'TZ' : 'Canada/Eastern'},
    'eu-central-1' : {'Title' : 'Frankfurt', 'TZ' : 'Europe/Berlin'},
    'eu-west-1' : {'Title' : 'Ireland', 'TZ' : 'Europe/Dublin'},
    'eu-west-2' : {'Title' : 'London', 'TZ' : 'Europe/London'},
    'eu-west-3' : {'Title' : 'Paris', 'TZ' : 'Europe/Paris'},
    'sa-east-1' : {'Title' : 'São Paulo', 'TZ' : 'America/Sao_Paulo'},
    'us-joke-1' : {'Title' : 'Roswell, NM', 'TZ' : 'US/Mountain'}
}

@application.route('/api/v1.0/get_zones', methods=['GET'])
def get_zones():
    "Returns a list of regions / timezones"
    zones = {'zones' : dict(ZONES)}
    if "HOSTNAME" in os.environ:
        zones["hostname"] = os.environ["HOSTNAME"]
    return jsonify(zones)

@application.route('/api/v1.0/get_current_time/<path:region>', methods=['GET'])
def get_current_time(region):
    "Returns the current time in region / timezone"
    tz_tz = pytz.timezone(ZONES[region]['TZ'])
    tz_now = datetime.now(tz_tz)
    response = {"region" : region, "now" : tz_now.strftime("%H:%M:%S %Z")}
    if "HOSTNAME" in os.environ:
        response["hostname"] = os.environ["HOSTNAME"]
    return jsonify(response)

if __name__ == "__main__": # pragma: no cover
    application.run(debug=True, host='0.0.0.0', port=8081)
