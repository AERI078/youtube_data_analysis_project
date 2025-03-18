import os
import time
import pandas as pd

from mypackage import get_youtube_object

# global variables
MAX_RESULTS = 10
DATA_FILE_PATH = 'youtube_video_data.csv'
# DATA_FILE_PATH = 'test.csv'

""" !!!!!!!!!! BEFORE RUNNING CHECK !!!!!!!!!!!!!! ----------------------------------------
1. MAX_RESULTS
2. REGION CODE LIST
3. DATA FILE PATH
-------------------------------------------------------------------------------------------
"""

def main():
    youtube = get_youtube_object()

    columns = ['id', 'region_code', 'publish_date', 'channel_id', 'channel_name',
                'title', 'description', 'category_id', 'duration', 'caption', 'views',
                'likes', 'comment_count']

    data = []
    
    # countries having the highest number of youtube users -> ['IN', 'US', 'BR', 'ID', 'MX']
    for region_code in ['IN', 'US', 'BR', 'ID', 'MX']:
        data.extend(get_data(youtube, region_code))
        time.sleep(2)

    df = pd.DataFrame(data, columns=columns)

    write_header = not os.path.exists(DATA_FILE_PATH)

    df.to_csv(DATA_FILE_PATH, mode='a', header=write_header, index=False)




# Get data for a region code and return it in the form of list of dicts
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

    # to check number of pages in response
    print(response['pageInfo']['totalResults'])
    print(response['pageInfo']['resultsPerPage'])

    return data_list


if __name__ == "__main__":
    main()
