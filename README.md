# Valheim-Logger

This is a simple Python script designed for Linux-based Valheim Dedicated Servers. It will search the Valheim log to look for connect and disconnect messages from players. If it finds one, it will send a text alert to a Discod webhook.

## Installation

1. Copy the **connections.py** and **connections_config.ini** files into your server's `/valheim` folder - this is usually at `/home/steam/valheim`.

2. Edit the **connections_config.ini** file and set the following values:
      - ***webhookurl*** - The unique webhook URL for your Discord bot. Review https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks if you need help creating a webhook.
      
      - ***logdir*** - The absolute path to your Valheim log file, default is `/home/steam/valheim/valheim_log.txt`. 
        - *Tip:* If you do not have one, create a log file by piping the output of the Valheim start script to a new file like this: `/start_server.x86_64 >> /home/steam/valheim/valheim_log.txt`.
      
      - ***servername*** - The name of your server the alert will mention.
      
      - ***tail_lines*** - The amount of lines from the Valheim log the script will search every time it runs. Default value is 50, only increase this value if new connections are not triggering alerts.
      
 3. (Optional) Add usernames and their unique Steam IDs to the `[SteamIDs]` section of the config file.
      - It is recommended you add a list of the most frequent players on the server to this section. Steam IDs can be found on a player's Steam Profile.
      - Add names in the following format, one per line:
      - `Username = SteamID`
      
 4. Save the changes made to the config file, then create a cronjob to run the script every few minutes. Busier servers should run the script every minute to avoid missing connections, while slower servers can run the script every 5 minutes.
      - Use `crontab -e` to edit the current user's crontab, then add one of the lines below.
      - For every minute:
      - `* * * * * /home/steam/valheim/connections.py`
      - For every 5 minutes:
      - `*/5 * * * * /home/steam/valheim/connections.py`
      
 5. Save the crontab and that's it!
