#!/usr/bin/env python3

"""
This script is intended to find all connections to a server in the past x minutes, then post the found connections to a Discord webhook.

The script tails the /home/steam/valheim/valheim_log.txt file for the last 50 lines, and checks for any connect or disconnect messages. If it finds some, it will send them to Discord webhook.

This script is designed to run every 5 minutes to ensure:
    1) Speed - parsing the entire valheim_log.txt file every time we want to check for a connect or disconnect would take too many resources.
    2) No (dis)connects are missed. By tailing the last 50 lines of valheim_log.txt every 5 minutes, we should have a high degree of confidence nothing is missed

"""
import subprocess
import sys
import configparser as cp
import requests
from discord import Webhook, RequestsWebhookAdapter

### Import configuration from config.ini file and define functions

confdir = '/home/steam/valheim/connections_config.ini'
try:
    config = cp.ConfigParser()
    config.read(confdir)
    steam_ids = config['SteamIDs']
    steam_ids_list = list(steam_ids.values())
    steam_names_list = list(steam_ids.keys())
    URL = config['DEFAULTS']['WebhookURL']
    logdir = config['DEFAULTS']['LogDir']
    server = config['DEFAULTS']['servername']
    n = config['DEFAULTS']['Tail_lines']
except:
    print("Configuration file is missing, incorrect, or corrupt. Quitting...")
    sys.exit(1)

def runcmd(cmd):
    subprocess.Popen(cmd, shell=True)
    r = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = r.communicate()
    return stdout

def set_connect(name, flag):
    config['Connections'][name] = str(flag)
    with open(confdir, 'w') as cfg:
        config.write(cfg)

def set_disconnect(name, flag):
    config['Disconnects'][name] = str(flag)
    with open(confdir, 'w') as cfg:
        config.write(cfg)

### Tail the log file and get the output
tail = "tail -n " + n + " " + logdir
log = str(runcmd(tail))

### Assemble alert text and data
new_con = "Got connection SteamID "
end_con = "Closing socket "
alert = []
bold="**"
ctext = "** connected to " + server + "!"
etext = "** disconnected from " + server + "!"
uctext = "**Unknown user** connected to " + server + "!"
uetext = "**Unknown user** disconnected from " + server + "!"

# Check if the following line is in the log:
# Got connection SteamID xxxxxxxxxxxxxxx

# Assumes multiple unknown connections did not occur simultaneously

# Each successful alert writes a boolean flag to the config file, preventing alert spam
# Any time the script does not find any alerts to send, it resets all those flags to False

if new_con in log:
    if len(steam_names_list) != 0:
        for name in steam_names_list:
            try:
                if steam_ids[name] in log and config['Connections'][name] != "True":
                    text = bold + name + ctext
                    alert.append(text)
                    set_connect(name, True)
                else:
                    continue
            except KeyError:
                set_connect(name, False)
                continue
        else:
            if len(alert) == 0 and "True" not in list(config['Connections'].values()):
                alert.append(uctext)
    else:
        alert.append(uctext)
else:
    for name in steam_names_list:
        set_connect(name, False)

if end_con in log:
    if len(steam_names_list) != 0:
        for name in steam_names_list:
            try:
                if steam_ids[name] in log and config['Disconnects'][name] != "True":
                    text = bold + name + etext
                    alert.append(text)
                    set_disconnect(name, True)
                else:
                    continue
            except KeyError:
                set_disconnect(name, False)
                continue
        else:
            if len(alert) == 0 and "True" not in list(config['Disconnects'].values()):
                alert.append(uetext)
    else:
        alert.append(uetext)
else:
    for name in steam_names_list:
        set_disconnect(name, False)


### Post alert text to the Discord webhook
webhook = Webhook.from_url(URL, adapter=RequestsWebhookAdapter())

if len(alert) == 0:
    print("No alerts to post, quitting...")
    sys.exit(1)
else:
    for text in alert:
        webhook.send(text)
