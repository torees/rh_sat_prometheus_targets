#!/usr/bin/env python



import argparse
from datetime import datetime
import ConfigParser
import json
import os
import urllib2
import urllib

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
from collections import OrderedDict

base_url = {{sat_base_url}}
username = {{sat_username}}
password = {{sat_password}}
verifyTLS = {{sat_verifyTLS}}
hostgroup = {{sat_hostgroup}}

api_path = "/api/v2/hosts"

def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    api_data = []
    page = 0
    per_page = 100
    url = base_url + api_path 
    try:
        while True:
            page += 1
            
            resp = requests.get(
                url,
                params = {
                    'page': page,
                    'per_page': per_page
                    },
                auth=HTTPBasicAuth(username,password),
                verify=verifyTLS
            )
            resp.raise_for_status()
            
            hosts = resp.json()['results']
            
            if not hosts:                
                break
           
            api_data.append(hosts)
    
    except urllib2.URLError, e:
        print ("Cannot connect to Satelite API. Verify network")
        
    
    
    targets_list = []
    host_object_list = api_data  
    
    for i in range(len(host_object_list)-1):
        for host_item in host_object_list[i]:
            
            if isinstance(host_item['hostgroup_title'],unicode):
                if hostgroup in host_item['hostgroup_title']:
                    target = { 
                        "targets" : [ host_item['name'] + ':9100'] , 
                        'labels' : { 
                            'hostgroup' : host_item['hostgroup_name'], 
                            'ip' : host_item['ip'], 
                            "__metrics_path__": "/metrics",
                            "environment": host_item['content_facet_attributes']['lifecycle_environment_name'],
                            "location" : host_item['location_name'] 
                            }  
                        }
                    targets_list.append(target)
            

   

    
    with open('targets.json','w') as f:
        json.dump(targets_list,f,indent=4)
main()

