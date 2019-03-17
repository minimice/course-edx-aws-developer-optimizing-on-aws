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
"Front end for timezones application"
import os
from flask import Flask, render_template
import api

application = Flask(__name__)

@application.route("/", defaults={'region': None})
@application.route("/<path:region>")
def home(region):
    "Home route"
    zones = api.get_zones()
    hostname = os.environ["HOSTNAME"] if "HOSTNAME" in os.environ else None
    current_time = None
    if region:
        current_time = api.get_current_time(region)
    return render_template("main.html",
                           zones=zones['zones'],
                           hostname=hostname,
                           region=region,
                           current_time=current_time)

if __name__ == "__main__": # pragma: no cover
    application.run(debug=True, host='0.0.0.0', port=8080)
