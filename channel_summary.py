import logging

logging.basicConfig(filename = 'scrapper.log', filemode = 'w', level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')


def get_channel_stats(youtube, channel_id):
    '''
    This function will return us the statistics of YouTube channel we are trying to search
    :param youtube:<googleapiclient.discovery.Resource at 0x1601bd94b50>
    :param channel_id: It will return the overall stat of channel
    :return: type: <Dictionary>, The dictionary contains all the required data fetched using youtube api
    '''
   
    try:
        request = youtube.channels().list(part = 'snippet,contentDetails,statistics', id = channel_id)

        response = request.execute()

        channel_stats = dict(
            channel_id      = response['items'][0]['id'],
            Title           = response['items'][0]['snippet']['title'],
            playlist_id     = response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
            viewCount       = int(response['items'][0]['statistics']['viewCount']),
            subscriberCount = int(response['items'][0]['statistics']['subscriberCount']),
            videoCount      = int(response['items'][0]['statistics']['videoCount']))

        logging.info(channel_stats)
        return channel_stats
    except Exception as e:
        logging.error ('Unable to retrieve information. Please Check again')


if __name__ == '__main__':
    from googleapiclient.discovery import build
    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_service_name = "youtube"
    api_version = "v3"
    api = os.getenv('inr')
    api_key = f'{api}'
    channel_id  = 'UCNU_lfiiWBdtULKOw6X0Dig'
    youtube = build(api_service_name, api_version, developerKey = api_key)
    
    get_channel_stats(youtube, channel_id)