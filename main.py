import os
from datetime import datetime
import pytz
import docker
import requests
import time

time_interval_seconds = os.environ.get('time_interval_seconds')
restart_docker_container_url = os.environ.get('restart_docker_container_url')


def restart_containers():
    try:
        response = requests.get(restart_docker_container_url)
        if response.status_code == 200:
            send_telegram_message_to_admin("All docker containers has been restarted.")
    except Exception as ex:
        print("Error occurred in restart_containers: - " + str(ex))
        send_telegram_message_to_admin("unable to restart container. Error message - {}".format(str(ex)))


def send_telegram_message_to_admin(message):
    telegram_bot_url = "https://api.telegram.org/bot1724891059:AAEM2uFkNV8iLPjM637S6FndW4w20WKW9Ro/sendMessage" \
                       "?chat_id=@affsolution&text=" + message
    response = requests.post(telegram_bot_url)
    return response


if __name__ == "__main__":
    #eastern = pytz.timezone('Asia/Kolkata')
    # india_time_zone = pytz.timezone('Asia/Kolkata')
    # ams_dt = loc_dt.astimezone(india_time_zone)

    import pytz

    tz = pytz.timezone('Asia/Kolkata')
    ist_time_now = datetime.now(tz)

    start_time = time.time()
    if restart_docker_container_url is None:
        raise Exception("Please specify the docker URL")
    while True:
        if ist_time_now.hour == 2:
            send_telegram_message_to_admin("WhatsApp Container Restart Job Started..")
            restart_containers()
            send_telegram_message_to_admin("WhatsApp Container Restart Job Completed.")
            if time_interval_seconds is None:
                time_interval_seconds = 43200
            time.sleep(int(time_interval_seconds) - ((time.time() - start_time) % int(time_interval_seconds)))
