#!/usr/bin/env python3

import braketology
import boto3

s3_bucket_name = braketology.get_s3_folder(None)[0]

s3_bucket_name = s3_bucket_name + 'xy'

print()
print(f'Checking for s3 bucket... {s3_bucket_name}')

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

s3_bucket = s3.Bucket(s3_bucket_name)

if s3_bucket in s3.buckets.all():
    print('Bucket already exists. Ready to run experiments.')
else:
    print('Creating bucket...')
    s3_bucket.create()
    print('Bucket created. Ready to run experiments.')


print()