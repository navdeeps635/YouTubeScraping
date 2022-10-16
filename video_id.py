from json import load
import logging

logging.basicConfig(filename = 'scrapper.log', filemode = 'w', level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')


def get_video_ids(youtube, channel_summary):
    
    '''
    This function will return all the video ids associated with playlist_id of specific channel
    :param youtube:  <googleapiclient.discovery.Resource at 0x1601bd94b50>
    :param playlist_id: <dict> of <list> it contains all the video Id from a channel
    :return: video_ids of all the videos associated with playlist_id 
    '''

    try:
        all_video_ids = []
        request = youtube.playlistItems().list(
            part = 'contentDetails',
            playlistId = channel_summary['playlist_id'],
            maxResults = 50)
        
        response = request.execute()
        
        for i in range(len(response['items'])):
             video_id = response['items'][i]['contentDetails']['videoId']
             all_video_ids.append(video_id)

        data = dict(channel_id = channel_summary['channel_id'],
                    video_ids = all_video_ids)
        logging.info('video ids are fetched')
        logging.info(data)
        return data
    except Exception as e:
        logging.error('An error occured',e) 

if __name__ == '__main__':
    from googleapiclient.discovery import build
    from channel_summary import get_channel_stats
    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_service_name = "youtube"
    api_version = "v3"
    api = os.getenv('inr')
    api_key = f'{api}'
    channel_id  = 'UCNU_lfiiWBdtULKOw6X0Dig'
    youtube = build(api_service_name, api_version, developerKey = api_key)
    channel_summary = get_channel_stats(youtube,channel_id)
    get_video_ids(youtube,channel_summary)