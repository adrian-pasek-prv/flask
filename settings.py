# This settings file will be used by Render.com when we run rq worker -c settings there
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
QUEUES = ['emails', 'default']