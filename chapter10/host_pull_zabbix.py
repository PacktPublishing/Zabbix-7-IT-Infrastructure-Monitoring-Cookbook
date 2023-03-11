import requests
import json

#General Zabbix parameters. Remove username and password after API token is generated!
zabbix_url = "https://myzabbix.com/api_jsonrpc.php"
zabbix_username = "username"
zabbix_password = "password"


#Function to request API token
def get_api_token(url):

    payload = {
        "jsonrpc":"2.0",
        "method":"user.login",
        "params":{"user":zabbix_username,"password":zabbix_password},
        "id": 1,
        "auth": None
    }

    resp = requests.post(url=url, json=payload )
    out = resp.json()

    return out['result']


#Function to retrieve all hosts from Zabbix
def get_hosts(api_token, url):

    payload = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": [
            "hostid",
            "host"
        ],
        "selectInterfaces": [
            "interfaceid",
            "ip",
            "main"
        ]
    },
    "id": 2,
    "auth": api_token
    }

    resp = requests.post(url=url, json=payload )
    out = resp.json()

    return out['result']


#Write results to host file
def generate_host_file(hosts,host_file):

    hostname = None
    f = open(host_file, "w")

    #As the hostfile is overwritten on each call, write the defaults first:

    #For Debian based hosts
    f.write('''127.0.0.1 localhost\n\n''')

    #For RHEL based hosts
    #f.write('''127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
#::1         localhost localhost.localdomain localhost6 localhost6.localdomain6\n\n''')

# The following lines are desirable for IPv6 capable hosts
    f.write('''::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters\n\n\n''')


    #Write host entries from Zabbix
    for host in hosts:
        hostname = host['host']
        for interface in host["interfaces"]:
            if interface["main"] == "1":
                f.write(hostname + " " + interface["ip"] + "\n")

    f.close()
    return



#If you do not have a API token yet, use the following line to aquire it.
#Once printed, copy the token and paste it in the variable below.

#print(get_api_token(zabbix_url))

api_token = "cqfgye7aasXimVrBpGeuoUimnsjABpGw"

#once the API token has been set, comment the print line again and uncomment the follwoing lines. 

#zabbix_hosts = get_hosts(api_token,zabbix_url)
#generate_host_file(zabbix_hosts,"/etc/hosts")
