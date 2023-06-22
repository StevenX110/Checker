import asyncio
import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth
from telethon.errors import SessionPasswordNeededError

api_id = YOUR_API_ID  
api_hash = 'YOUR_API_HASH'  
session_file = 'session_name'  
target_username = 'TARGET_USERNAME'  
def analyze_online_time(user_status):
    if isinstance(user_status, UserStatusRecently):
        return 'Recently online'
    elif isinstance(user_status, UserStatusLastWeek):
        return 'Last week'
    elif isinstance(user_status, UserStatusLastMonth):
        return 'Last month'
    else:
        return 'Over a month ago'

async def status_update_handler(event):
    if event.username.lower() == target_username.lower():
        if isinstance(event.status, UserStatusLastMonth):
            offline_time = datetime.datetime.now() - event.status.was_online
            offline_days = offline_time.days
            offline_hours = offline_time.seconds // 3600
            offline_minutes = (offline_time.seconds // 60) % 60
            offline_seconds = offline_time.seconds % 60

            print('User has gone off:', datetime.datetime.now())
            print('How much time did it take:', analyze_online_time(event.status))
            print('Offline stat: {} days, {} hours, {} minutes, {} seconds'.format(offline_days, offline_hours, offline_minutes, offline_seconds))
            print('Date and time:', event.status.was_online.strftime('%Y-%m-%d %H:%M:%S'))

client = TelegramClient(session_file, api_id, api_hash)

try:
    client.start()
except SessionPasswordNeededError:
    client.start(password=input('Type in your password: '))

client.add_event_handler(status_update_handler)

client.run_until_disconnected()
