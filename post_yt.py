import os
import json
from pprint import pprint
from time import sleep
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


# Google Helper Library Settings
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Authentication Process
scopes = ["https://www.googleapis.com/auth/youtube"]

client_secrets_file = os.environ.get("CLIENT_SECRETS_FILE_PATH")
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=flow.run_console())


# Loads Video Ids then runs requests
with open("video_ids.json", "r") as in_file:

    # Get playlist id from url
    playlist_id = "PLFzzCTS-4gnz5xEOtzBTlTUcK6ZDXQzGq"
    video_ids = json.load(in_file)['video_ids']

    for video_id in video_ids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()
        time.sleep(0.1)
        print(f"Added {response['snippet']['title']} to the playlist")



