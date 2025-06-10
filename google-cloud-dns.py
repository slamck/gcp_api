# scriptlet of GCP API - Python Client for Cloud DNS API
#
# Install google-cloud-dns on Mac/Linux:
# pip install virtualenv
# virtualenv <your-env>
# source <your-env>/bin/activate
# <your-env>/bin/pip install --upgrade google-api-python-client google-auth
#
# or use service account key file:
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/stelam1/.config/gcloud/five9-infrastructure-dev-fd8f8805b222.json"
#
# GCP API auth:
# https://googleapis.dev/python/google-auth/latest/user-guide.html
#
#  

import urllib3
urllib3.disable_warnings()
import json
import os
from pprint import pprint

from google.oauth2 import service_account
from googleapiclient import discovery


sa_data = { 
"type": os.environ.get('GCP_TYPE'),
"project_id": os.environ.get('GCP_PROJECT_ID'),
"private_key_id": os.environ.get('GCP_PRIVATE_KEY_ID'),
"private_key": os.environ.get('GCP_PRIVATE_KEY').replace('\\n', '\n'),
"client_email": os.environ.get('GCP_CLIENT_EMAIL'),
"token_uri": os.environ.get('GCP_TOKEN_URI')
}

# set credential and project
credentials = service_account.Credentials.from_service_account_info(sa_data)
service = discovery.build('dns', 'v1', credentials=credentials)
project = 'five9-infrastructure-dev'

# Create new private zone
managed_zone_body = {
  "name": "my-zone-01",
  "dnsName": "myzone01.local.",
  "description": "",
  "visibility": "private"
}
request = service.managedZones().create(project=project, body=managed_zone_body)
response = request.execute()
# print response
pprint(response)

# list zones
request = service.managedZones().list(project=project)
response = request.execute()
for managed_zone in response['managedZones']:
    pprint(managed_zone)

# list records in zone
managed_zone = 'my-zone'
request = service.resourceRecordSets().list(project=project, managedZone=managed_zone)
response = request.execute()
for resource_record_set in response['rrsets']:
    pprint(resource_record_set)

# get a record in zone
managed_zone = 'my-zone'
request = service.resourceRecordSets().get(
    project=project,
    managedZone=managed_zone,
    name='arecord123.myzone.local.',
    type='A'
    )
response = request.execute()
pprint(response)

# create new A record in zone
managed_zone = 'my-zone'
dns_record_body = {
    'kind': 'dns#resourceRecordSet',
    'name': 'arecord123.myzone.local.',
    'rrdatas': ['10.2.3.4'],
    'ttl': 300,
    'type': 'A'
}
request = service.resourceRecordSets().create(
    project=project,
    managedZone=managed_zone,
    body=dns_record_body
    )
response = request.execute()
pprint(response)

# delete record in zone
managed_zone = 'my-zone'
request = service.resourceRecordSets().delete(
    project=project,
    managedZone=managed_zone,
    name='arecord123.myzone.local.',
    type='A'
    )
response = request.execute()
pprint(response)

# update an existing record
managed_zone = 'my-zone'
dns_record_body = {
    'kind': 'dns#resourceRecordSet',
    'name': 'arecord123.myzone.local.',
    'rrdatas': ['10.2.3.40'],
    'ttl': 300,
    'type': 'A'
}
request = service.resourceRecordSets().patch(
    project=project,
    managedZone=managed_zone,
    name='arecord123.myzone.local.',
    type='A',
    body=dns_record_body
    )
response = request.execute()
pprint(response)

