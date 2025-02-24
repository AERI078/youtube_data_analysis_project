import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

# global variables
# region codes - 'US' 'IN' 'br' 'id' 'mx'
MAX_RESULTS = 10
REGION_CODE = 'MX'

def main():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyBH_tlmqqSWUGYTGHoWGTRlqFGONWOdLLo"

    youtube = auth(api_service_name, api_version, api_key)

    data = get_data(youtube)

    df = pd.DataFrame(data)
    df.to_csv('youtube_video_data.csv', mode='a', header=False)



# Create an API client
def auth(api_service_name, api_version, api_key):
    youtube = googleapiclient.discovery.build(
        serviceName=api_service_name, version=api_version, developerKey=api_key)
    return youtube

#  1st request object
def get_data(youtube):
    data_list = []

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics,id",
        chart="mostPopular",
        regionCode=REGION_CODE,
        maxResults=MAX_RESULTS
    )

    response = request.execute()

    # for i in range(MAX_RESULTS):


    data_dict = {
        "id" : response["items"][0]["id"],
        "region_code" : REGION_CODE,
        "publish_date" : response["items"][0]["snippet"]["publishedAt"],
        "channel_id" : response["items"][0]["snippet"]["channelId"],
        "title" : response["items"][0]["snippet"]["title"],
        "description" : response["items"][0]["snippet"]["description"],
        "channel_name" : response["items"][0]["snippet"]["channelTitle"],
        "category_id" : response["items"][0]["snippet"]["categoryId"],
        "duration" : response["items"][0]["contentDetails"]["duration"],
        "caption" : response["items"][0]["contentDetails"]["caption"],
        "views" : response["items"][0]["statistics"]["viewCount"],
        "likes" : response["items"][0]["statistics"]["likeCount"],
        "comment_count" : response["items"][0]["statistics"]["commentCount"],
        "next_page_token" : response['nextPageToken']
    }

    data_list.append(data_dict)
    next_page_token = response['nextPageToken']

    # other requests
    if((MAX_RESULTS - 1) == 0):
        return data_list
    
    for i in range(1, MAX_RESULTS):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics,id",
            chart="mostPopular",
            regionCode=REGION_CODE,
            maxResults=MAX_RESULTS,
            pageToken=next_page_token
        )

        response = request.execute()

        data_dict = {
            "id" : response["items"][i]["id"],
            "region_code" : REGION_CODE,
            "publish_date" : response["items"][i]["snippet"]["publishedAt"],
            "channel_id" : response["items"][i]["snippet"]["channelId"],
            "title" : response["items"][i]["snippet"]["title"],
            "description" : response["items"][i]["snippet"]["description"],
            "channel_name" : response["items"][i]["snippet"]["channelTitle"],
            "category_id" : response["items"][i]["snippet"]["categoryId"],
            "duration" : response["items"][i]["contentDetails"]["duration"],
            "caption" : response["items"][i]["contentDetails"]["caption"],
            "views" : response["items"][i]["statistics"]["viewCount"],
            "likes" : response["items"][i]["statistics"]["likeCount"],
            "comment_count" : response["items"][i]["statistics"]["commentCount"],
            "next_page_token" : response['nextPageToken']
        }

        data_list.append(data_dict)

    print(response['pageInfo']['totalResults'])
    print(response['pageInfo']['resultsPerPage'])

    return data_list

if __name__ == "__main__":
    main()
