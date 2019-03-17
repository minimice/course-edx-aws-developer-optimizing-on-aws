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
from __future__ import print_function
import boto3


dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Courses')

for item in range(1,1000):

    response = table.put_item(
       Item={
    		"subject": "Art History" + str(item),
            "school": "School of Humanities & Sciences",
            "course_name": "American Architecture",
            "info": {
                "code": "ARTHIST 143A",	
                "units": 1,
                "terms": [
                    "Autumn",
    				"Winter",
                    "Spring",
                    "Summer"
                ],
                "course_url": "http://explorecourses.stanford.edu/search?view=catalog&academicYear=&page=0&q=ARTHIST&filter-departmentcode-ARTHIST=on&filter-coursestatus-Active=on&filter-term-Spring=on",
                "description": "A historically based understanding of what defines American architecture.",
    			"grading": "Letter (ABCD/NP)",
    			"notes": "None",
                "instructors": [
                    "Beischer, T. (PI)"
                ]
            }
        }
    )
    print("PutItem succeeded:")