import mysql.connector as conn
import pandas as pd
import logging

logging.basicConfig(
    filename = 'scrapper.log',
    filemode = 'w',
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')

def save_to_MySQL():
    '''
    This function will establish connection with MySQL and store data in database there.
    ''' 
    try:
        mydb = conn.connect(host = 'localhost', user = 'root', passwd = 'Gate@7172')
        logging.info('Connection established with MySQL')
        cursor = mydb.cursor()
    except Exception as e:
        logging.error(f'An error occured:{e}')
    try:
        cursor.execute('create database if not exists YouTube_data')
        cursor.execute('''create table if not exists YouTube_data.youtube_table (YouTuber varchar(50),
        Video_title varchar (100), PublisedAt varchar(50), Video_id varchar(100), Video_link varchar(100),
        view_count int(10), like_count int(10), comment_count(10)''')
        # cursor.execute('insert into YouTube_data.youtube_table values ')
    except Exception as e:
        logging.error(f'An error occured:{e}')