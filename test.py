from dotenv import load_dotenv 
import os

load_dotenv()
a = os.getenv('mongo_pass')
psd = f'{a}'

print(psd)