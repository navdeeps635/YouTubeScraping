import logging

logging.basicConfig(filename = 'scrapper.log', filemode = 'w', level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')

def get_video_details(youtube, video_id):
    '''
    This funtion will return the information about each video the channel such as video_title, views, likes and comments etc.
    :params you tube: <googleapiclient.discovery.Resource at 0x1601bd94b50>
    :param video_id : <dict> of <list> it contains all the video Id from a channel
    :return: information about each video of specific video_id
    '''
    try:

        video_data = []
        request = youtube.videos().list(part = 'snippet,statistics', id = ','.join(video_id['video_ids']))

        response = request.execute()
        
        for i in range(len(response['items'])):
            video_info = dict(
            channel_id   = video_id['channel_id'],
            video_title  = response['items'][i]['snippet']['title'],
            thumbnail    = response['items'][i]['snippet']['thumbnails']['high']['url'],
            viewcount    = int(response['items'][i]['statistics']['viewCount']),
            likecount    = int(response['items'][i]['statistics']['likeCount']),
            commentcount = int(response['items'][i]['statistics']['commentCount']),
            video_link   = 'https://www.youtube.com/watch?v=' + response['items'][i]['id'],
            video_id     = response['items'][i]['id'])

            video_data.append(video_info)

        logging.info('video datails are fetched')
        return video_data   

    except Exception as e:
        logging.error('An error has occured',e)

if __name__ == '__main__':
    from googleapiclient.discovery import build
    from channel_summary import get_channel_stats
    from video_id import get_video_ids
    api_service_name = "youtube"
    api_version = "v3"
    api_key = 'AIzaSyDngNny8jHygqybN7XXlQtGtR0cefNmGrI'
    channel_id  = 'UCNU_lfiiWBdtULKOw6X0Dig'
    youtube = build(api_service_name, api_version, developerKey = api_key)
    channel_summary = get_channel_stats(youtube,channel_id)
    video_id = get_video_ids(youtube,channel_summary)
    #video_ids = ['Td-Qq2xwG64','OK-7VsVVej','Hgjax-GPsA','5W9QiJo95Ws']

    get_video_details(youtube,video_id)

