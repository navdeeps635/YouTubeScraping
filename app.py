from flask import Flask, render_template, request, redirect, send_file
from googleapiclient.discovery import build
from channel_summary import get_channel_stats
from save_thumbnail import save_image
from video_id import get_video_ids
from video_details import get_video_details
from video_details import get_vid_details
from comments import get_comments
from pytube import YouTube
import mysql.connector as conn
import pymongo
from io import BytesIO
from dotenv import load_dotenv 
import os

import logging

logging.basicConfig(
    filename='scrapper.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s-%(levelname)s-%(name)s-%(message)s')
try:
    load_dotenv()
    api_service_name = "youtube"
    api_version = "v3"
    api = os.getenv('inr')
    api_key = f'{api}'
    youtube = build(api_service_name, api_version, developerKey=api_key)

    ini = os.getenv('mgo_pass')
    client = pymongo.MongoClient(
        f"mongodb+srv://navdeep3135:{ini}@cluster0.lgvqzwx.mongodb.net/?retryWrites=true&w=majority")
    db = client.youtube

    channel_coll = db['channel_table']
    video_coll = db['video_table']
    comm_coll = db['comments_data']

except Exception as e:
    logging.error(e)


class channel:
    channel_id = ''


obj_ytube = channel()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homePage():
    '''
    :return: It returns the index.html template
    '''
    try:
        return render_template('index.html')
    except Exception as e:
        return render_template('error.html')


@app.route('/youtube_path', methods=['POST'])
def find_channel_id():
    '''
    This function will return youtube channel Id with the help of pytube module
    :return: none, redirect to /channel_summary
    '''
    try:
        video = YouTube(request.form['url'])
        obj_ytube.channel_id = video.channel_id

        return redirect('/channel_summary')
    except Exception as e:
        return render_template('error.html')


@app.route('/channel_summary', methods=['GET'])
def channel_summary():
    '''
    This function will return us the stats of data.
    '''
    try:
        channel_summary = get_channel_stats(youtube, obj_ytube.channel_id)

        channel_coll.insert_one(channel_summary)
        video_ids = get_video_ids(youtube, channel_summary)
        video_details = get_video_details(youtube, video_ids)
        comment_table = get_comments(youtube,video_details)

        for i in video_details:
            video_coll.insert_one(i)
        
        return redirect('/list_channel')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')


@app.route('/list_channel', methods=['GET'])
def list_channel():
    '''
    This function will fetch the channel details from DB
    :return: channel.html
    '''
    try:
        record = channel_coll.find()
        return render_template('channel.html', var=record)
    except Exception as e:
        logging.error(e)
        return render_template('error.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path>')
def catch_all(path):
    '''
    This function is used to fetch all the stored video info from MYSQL DB
    :param path: channel_id
    :return: video_html
    '''

    try:
        record = video_coll.find({'channel_id': path})

        return render_template('videos.html', var=record)
    except Exception as e:
        logging.error(e)
        return render_template('error.html')


@app.route('/videos/', defaults={'path': ''})
@app.route('/videos/<path:path>')
def comments(path):
    '''
    This function is used to fetch all the comments from MongoDB
    :param path: video_id
    :return: video_html
    '''

    try:
        a = comm_coll.find()

        for i in a:
            if i['video_id'] == path:

                return render_template('comment.html', var=i['comments_id']['comments'])

        else:
            vid_details = get_vid_details(youtube, path)
            comment_table = get_comments(youtube, vid_details)
            img_b64 = save_image(vid_details)

            for i in range(len(img_b64)):
                data_mongo = {
                    'video_Id': img_b64[i]['video_id'],
                    'img_base64_encoded': img_b64[i]['img_b64'],
                    'comments_id': comment_table[i]}

                comm_coll.insert_one(data_mongo)
                return redirect(f'/videos/{path}')
        return render_template('base.html')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')


@app.route('/download/', defaults={'path': ''})
@app.route('/download/<path:path>')
def download_video(path):
    '''
    this function is used to download the youtube video
    :param path: video_id
    :return: NONE redirect to the /list_channel
    '''
    try:
        buffer = BytesIO()

        path = 'https://www.youtube.com/watch?v=' + path
        video = YouTube(path)
        video = video.streams.get_highest_resolution()
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='video.mp4', mimetype='video/mp4')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')


@app.route('/image/', defaults={'path': ''})
@app.route('/image/<path:path>')
def image(path):
    '''
    this function is used to download the youtube video
    :param path: video_id
    :return: NONE redirect to the /list_channel
    '''
    try:
        a = comm_coll.find()

        for i in a:
            if i['video_id'] == path:
                return render_template('images.html', image=i['img_base64_encoded'])
        return render_template('base.html')
    except Exception as e:
        logging.error(e)
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True,port = 5001)
