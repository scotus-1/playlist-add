import os
import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
from time import sleep
from pprint import pprint
from json import dumps


# create global keys and secrets
discord_endpoint = "https://discord.com/api/v9"
bot_token = os.environ.get("BOT_TOKEN")
music_thread_id = "881599311132098570"

# discord headers
request_headers = {
    "Authorization": "Bot " + bot_token,
    "User-Agent": "music bot thing playlist v1.0.0"
}

current_message_id = None
video_ids = []
while True:
    response = requests.get(f'%s/channels/{music_thread_id}/messages' % discord_endpoint,
                            headers=request_headers,
                            params={'before': current_message_id,
                                    'limit': 100})

    if response.json():
        for message in response.json():
            if not isinstance(message, str):
                current_message_id = message['id']
                for embed in message['embeds']:
                    if embed['url'].startswith('https://www.youtube.com'):
                        parsed_yt_link = urlparse(embed['url'])
                        video_id = parse_qs(parsed_yt_link.query)['v'][0]
                        video_ids.append(video_id)
    else: break


    sleep(0.5)


video_ids.reverse()
json_string = dumps({"video_ids": video_ids}, indent=4)
with open("video_ids.json", "w") as outfile:
    outfile.write(json_string)





