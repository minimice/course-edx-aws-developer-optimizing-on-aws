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
"Demo Flask application"
import json
import time
import boto3
import memcache

from flask import Flask, render_template

import config

application = Flask(__name__)

attrs = """vcpu
storage
memory
processorFeatures
networkPerformance
processorArchitecture
ecu
tenancy
instanceFamily
licenseModel
preInstalledSw
clockSpeed
physicalProcessor""".split('\n')

instance_types = """t2.nano
t2.micro
t2.small
t2.medium
t2.large
t2.xlarge
t2.2xlarge
m5.large
m5.xlarge
m5.2xlarge
m5.4xlarge
m5.12xlarge
m5.24xlarge
m4.large
m4.xlarge
m4.2xlarge
m4.4xlarge
m4.10xlarge
m4.16xlarge
c5.large
c5.xlarge
c5.2xlarge
c5.4xlarge
c5.9xlarge
c5.18xlarge
c4.large
c4.xlarge
c4.2xlarge
c4.4xlarge
c4.8xlarge
f1.2xlarge
f1.16xlarge
g3.4xlarge
g3.8xlarge
g3.16xlarge
g2.2xlarge
g2.8xlarge
p2.xlarge
p2.8xlarge
p2.16xlarge
p3.2xlarge
p3.8xlarge
p3.16xlarge
r4.large
r4.xlarge
r4.2xlarge
r4.4xlarge
r4.8xlarge
r4.16xlarge
x1.16xlarge
x1e.xlarge
x1e.2xlarge
x1e.4xlarge
x1e.8xlarge
x1e.16xlarge
x1e.32xlarge
x1.32xlarge
d2.xlarge
d2.2xlarge
d2.4xlarge
d2.8xlarge
i2.xlarge
i2.2xlarge
i2.4xlarge
i2.8xlarge
h1.2xlarge
h1.4xlarge
h1.8xlarge
h1.16xlarge
i3.large
i3.xlarge
i3.2xlarge
i3.4xlarge
i3.8xlarge
i3.16xlarge""".split('\n')

filters = [
    {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': 'US East (N. Virginia)'},
    {'Type': 'TERM_MATCH', 'Field': 'licenseModel', 'Value': 'No License required'},
    {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
    {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
    {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'}
]

@application.route("/", methods=('GET', 'POST'))
def home():
    "Homepage route"
    return render_template("main.html",
                           filters=filters,
                           instance_types=instance_types)

@application.route("/clear_cache")
def clear_cache():
    "clear cache route"
    cache = memcache.Client([config.MEMCACHED_HOST])
    cache.flush_all()
    return render_template("main.html",
                           filters=filters,
                           instance_types=instance_types)

@application.route("/<instance_type>")
def instance_info(instance_type):
    "retrieve pricing info"
    pricing = boto3.client('pricing', region_name='us-east-1')
    cache = memcache.Client([config.MEMCACHED_HOST])

    instance_filters = filters[:]
    instance_filters.append(
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type}
    )

    # check the cache
    prices_json = cache.get(instance_type)
    sequence = """
    sequenceDiagram
    """
    sequence += "  App->>Cache: get %s\n" % instance_type
    start = time.time()  # start the timer

    # not in the cache
    if not prices_json:
        sequence += "  Cache->>App: cache miss 😕\n"
        sequence += "  App->>API: request price %s\n" % instance_type
        sequence += "  API->>App: response price %s\n" % instance_type

        # query the API
        prices_json = pricing.get_products(ServiceCode='AmazonEC2', Filters=instance_filters)
        sequence += "  App->>Cache: set %s\n" % instance_type

        # cache the results for 60 seconds
        cache.set(instance_type, prices_json, time=60)
        diff_seconds = time.time() - start
        diff_miliseconds = diff_seconds * 1000
        sequence += "  Note right of API: Completed in %.2fms" % diff_miliseconds
    else:
        sequence += "  Cache->>App: cache hit! 😀\n"
        diff_seconds = time.time() - start
        diff_miliseconds = diff_seconds * 1000
        sequence += "  Note right of Cache: Completed in %.5fms" % diff_miliseconds


    prices = json.loads(prices_json['PriceList'][0])
    info_dict = {key: prices['product']['attributes'][key] for key in attrs
                 if key in prices['product']['attributes']}
    price_dimensions = [prices['terms']['OnDemand'][key]["priceDimensions"][offerkey]
                        for key in prices['terms']['OnDemand'].keys()
                        for offerkey in prices['terms']['OnDemand'][key]["priceDimensions"].keys()]

    return render_template("main.html",
                           filters=filters,
                           attributes=info_dict,
                           instance_types=instance_types,
                           selected_instance_type=instance_type,
                           price_dimensions=price_dimensions,
                           sequence=sequence)


if __name__ == "__main__":
    # http://flask.pocoo.org/docs/0.12/errorhandling/#working-with-debuggers
    # https://docs.aws.amazon.com/cloud9/latest/user-guide/app-preview.html#app-preview-share
    use_c9_debugger = False
    application.run(use_debugger=not use_c9_debugger, debug=True,
                    use_reloader=not use_c9_debugger, host='0.0.0.0', port=8080)
