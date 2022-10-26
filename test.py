import pymongo
from io import BytesIO
from dotenv import load_dotenv 
import os

load_dotenv()

ini = os.getenv('mgo_pass')
client = pymongo.MongoClient(f"mongodb+srv://navdeep3135:{ini}@cluster0.lgvqzwx.mongodb.net/?retryWrites=true&w=majority")
db = client.test 

data_tab = client['sample']
first_coll = data_tab['abc']
second_coll = data_tab['def']
third_coll = data_tab['ghi']

d = dict(Name = 'Navdeep',
         Age = 24)
        
first_coll.insert_one(d)
second_coll.insert_one(d)
third_coll.insert_one(d)