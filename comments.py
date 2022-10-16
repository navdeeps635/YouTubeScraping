import logging

logging.basicConfig(filename = 'scrapper.log',
                    filemode = 'w',
                    level = logging.DEBUG,
                    format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')

def get_comments(youtube,video_details):

    for id in video_details:

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=id['video_id'])
        response = request.execute()

        comment_table = []

        for item in response['items']:
                comments = dict(
                Comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay'],
                author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                        
                #comments.append(comment)
                #else:
                    #comments = []
                comment_table.append(comments)
        
        comments = dict(video_id = id['video_id'],
                        comments =  comment_table)
    logging.info('Comments are fetched')
    return comments
if __name__ == "__main__":
    from googleapiclient.discovery import build
    from channel_summary import get_channel_stats
    from video_id import get_video_ids
    from video_details import get_video_details
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
    video_ids = get_video_ids(youtube,channel_summary)
    video_details = get_video_details(youtube,video_ids)
    get_comments(youtube,video_details)