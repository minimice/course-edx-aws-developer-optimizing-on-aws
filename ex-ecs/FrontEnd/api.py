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
"Wrapper for API operations"
from urllib.parse import urljoin
import requests
import config

baseuri = config.APP_SERVER

def get_zones():
    "Wrapper for API get_zones"
    uri = urljoin(baseuri, '/api/v1.0/get_zones')
    return _get(uri)

def get_current_time(region):
    "Wrapper for API get_current_time"
    uri = urljoin(baseuri, '/api/v1.0/get_current_time/')
    uri = urljoin(uri, region)
    return _get(uri)

def _get(uri):
    resp = requests.get(uri)
    return resp.json()
