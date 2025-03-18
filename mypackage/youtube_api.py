import googleapiclient.discovery
import googleapiclient.errors

import os

def get_youtube_object():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get('YOUTUBE_API_KEY')

    youtube = googleapiclient.discovery.build(
        serviceName=api_service_name, version=api_version, developerKey=api_key)

    return youtube

