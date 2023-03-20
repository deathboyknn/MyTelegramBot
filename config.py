import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
def get_tg_token():
    return os.getenv('TG_TOKEN')

def get_cpm_token():
    return os.getenv('CPM_ID')