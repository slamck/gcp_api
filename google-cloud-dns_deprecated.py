# google-cloud-dns is incomplete and has a lot of features missing.  
# use Google Discovery API, google-api-python-client, instead.

# scriptlet of GCP API - Python Client for Cloud DNS API
#
# Install google-cloud-dns on Mac/Linux:
# pip install virtualenv
# virtualenv <your-env>
# source <your-env>/bin/activate
# <your-env>/bin/pip install google-cloud-dns
#
# Authenticate using GCP CLI:
# gcloud auth application-default login
# Credentials saved to file: [/Users/stelam1/.config/gcloud/application_default_credentials.json]

# GCP API auth:
# https://googleapis.dev/python/google-api-core/latest/auth.html
#
#  

import urllib3
urllib3.disable_warnings()
import json

# auth to google cloud
#import google.auth
#credentials, project = google.auth.default()

from google.cloud import dns

dns_client = dns.Client(project='five9-infrastructure-dev')

# list managed zones and records in project
zones = list(dns_client.list_zones())
for zone in zones:
    print(f"Zone Name: {zone.name}")
    print(f"DNS Name: {zone.dns_name}")
    print(f"Description: {zone.description}")
    print(f"Name Servers: {zone.name_servers}")
    print(f"Zone Path: {zone.path}")
    print(f"Project: {zone.project}")
    print("-----------------------------------------------")
    rr_set = list(zone.list_resource_record_sets())
    for rr in rr_set:
        print(f"  {rr.name} - {rr.record_type} - {rr.rrdatas} - {rr.ttl}")
    print("===============================================")

# create a new zone, public zone only
zone5 = dns_client.zone("my-zone-5", dns_name="myzone5.local.", description="my-zone-5")
zone5.create()
print(zone5.name)
print(zone5.dns_name)
print(zone5.zone_id)

