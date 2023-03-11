import requests
import json

#API login information
url = "http://10.16.16.152/zabbix/api_jsonrpc.php"
api_token = "PUT_YOUR_TOKEN_HERE"

#Add new code below here



#Add new code above here

#Generate hosts
zabbix_hosts = get_hosts(api_token,url)
generate_host_file(zabbix_hosts,"/home/results")
