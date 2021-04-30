#!/usr/bin/env python3

import boto3
import json
import sys

s3_url = sys.argv[1]

print()
print(f'Pulling results from: {s3_url}')
print()

bucket_name = s3_url.split('/')[2]
key = s3_url.split('/', 3)[3]

s3 = boto3.resource('s3')

s3_object = s3.Object(bucket_name, key)

data = json.loads(s3_object.get()['Body'].read().decode('utf-8'))

measurements = {}

for measurement in data['measurements']:
    measurement_key = str(measurement).replace('[','').replace(']','').replace(',','').replace(' ','')
    if measurement_key not in measurements:
        measurements[measurement_key] = 0
    measurements[measurement_key] += 1


print('Task completed with the following measurements:')
print()
print('  measurement ║    count    ')
print(' ═════════════╬═════════════')
for measurement in sorted(measurements):
    print(f'      {measurement}      ║     {measurements[measurement]}')
print()
