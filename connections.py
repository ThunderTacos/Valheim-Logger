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
from discord import SyncWebhook

### Import configuration from config.ini file and define functions
config = cp.ConfigParser()
config.read('config.ini')
steam_ids = config['SteamIDs']
URL = config['DEFAULTS']['WebhookURL']
logdir = config['DEFAULTS']['LogDir']
server = config['DEFAULTS']['servername']
n = config['DEFAULTS']['Tail_lines']

def runcmd(cmd)
    subprocess.Popen(cmd, shell=True)
    r = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = r.communicate()
    return stdout

### Tail the log file and get the output
tail = "tail -n " + n + " /home/steam/valheim/valheim_log.txt"
log = runcmd(tail)

### Assemble alert text and data
new_con = "Got connection SteamID "
end_con = "Closing socket "
alert = []
ctext = " connected to " + servername + "!"
etext = " disconnected from " + servername + "!"

if len(steam_ids) != 0:
    for key in steam_ids.keys():
        if (new_con + steam_ids[key]) in log:
            text = key + ctext
            alert.append(text)
            continue
        elif (end_con + steam_ids[keys]) in log:
            text = key + etext
            alert.append(text)
            continue
        elif new_con or end_con in log:
            text = "Unkown user (dis)connected to " + servername + "."
            alert.append(text)
        else:
            break
    else:
        if new_con or end_con in log:    
            text = "Unkown user (dis)connected to " + servername + "."
            alert.append(text)
        else:
            break
### Post alert text to the Discord webhook
webhook = SyncWebhook.from_url(URL)

if len(alert) == 0:
    break
    sys.exit(1)
else:
    for text in alert:
        webhook.send(text)
