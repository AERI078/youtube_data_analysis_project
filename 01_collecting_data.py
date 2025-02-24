import time
import os
import pandas as pd

import googleapiclient.discovery
import googleapiclient.errors

# global variables
MAX_RESULTS = 1
DATA_FILE_PATH = 'youtube_video_data.csv'
# DATA_FILE_PATH = 'test.csv'


def main():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyBH_tlmqqSWUGYTGHoWGTRlqFGONWOdLLo"

    youtube = auth(api_service_name, api_version, api_key)

    columns = ['id', 'region_code', 'publish_date', 'channel_id', 'channel_name',
                'title', 'description', 'category_id', 'duration', 'caption', 'views',
                'likes', 'comment_count']

    data = []
    # ['IN', 'US', 'BR', 'ID', 'MX']
    for region_code in ['IN', 'US', 'BR', 'ID', 'MX']:
        data.extend(get_data(youtube, region_code))
        time.sleep(10)

    df = pd.DataFrame(data, columns=columns)

    write_header = not os.path.exists(DATA_FILE_PATH)

    df.to_csv(DATA_FILE_PATH, mode='a', header=write_header, index=False)
    #df.to_csv('youtube_video_data.csv', mode='a', header=False)



# Create an API client
def auth(api_service_name, api_version, api_key):
    youtube = googleapiclient.discovery.build(
        serviceName=api_service_name, version=api_version, developerKey=api_key)
    return youtube


def get_data(youtube_object, region_code):
    data_list = []

    request = youtube_object.videos().list(
        part="snippet,contentDetails,statistics,id",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=MAX_RESULTS
    )

    response = request.execute()

    for i in range(MAX_RESULTS):
        data_dict = {
            "id" : response["items"][i]["id"],
            "region_code" : region_code,
            "publish_date" : response["items"][i]["snippet"]["publishedAt"],
            "channel_id" : response["items"][i]["snippet"]["channelId"],
            "channel_name" : response["items"][i]["snippet"]["channelTitle"],
            "title" : response["items"][i]["snippet"]["title"],
            "description" : response["items"][i]["snippet"].get("description", 0),
            "category_id" : response["items"][i]["snippet"]["categoryId"],
            "duration" : response["items"][i]["contentDetails"]["duration"],
            "caption" : response["items"][i]["contentDetails"]["caption"],
            "views" : response["items"][i]["statistics"].get("viewCount", 0),
            "likes" : response["items"][i]["statistics"].get("likeCount", 0),
            "comment_count" : response["items"][i]["statistics"].get("commentCount", 0)
        }

        data_list.append(data_dict)

    print(response['pageInfo']['totalResults'])
    print(response['pageInfo']['resultsPerPage'])

    return data_list

if __name__ == "__main__":
    main()
