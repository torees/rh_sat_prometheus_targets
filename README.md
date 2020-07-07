# rh_sat_prometheus_targets.py
Python script to fetch and parse client hosts from RH Satelite and format a targets.json file for prometheus scrape config. Currently formats for node_exporter, but will be updated 


#Parameters

You need to set the following parameters to use the script

base_url = "https://satelite.example.com" or "https://capsule.example.com:8443"
username = "my_read_user"
password = "my_password"
verifyTLS = True/False
hostgroup = "my_host_group"
