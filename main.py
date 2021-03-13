import os

import docker
import requests
import time

time_interval_seconds = os.environ.get('time_interval_seconds')


def restart_containers():
    try:
        client = docker.from_env()
        container_list = client.containers.list()
        if len(container_list) == 0:
            print("There are no running container available to restart.")
            send_telegram_message_to_admin("There are no running container available to restart.")
            return
        for container_obj in container_list:
            send_telegram_message_to_admin("{} is going to restart now".format(container_obj.name))
            container_obj.restart()
            send_telegram_message_to_admin("{} is restarted.".format(container_obj.name))
    except Exception as ex:
        send_telegram_message_to_admin("unable to restart container. Error message - {}".format(str(ex)))


def send_telegram_message_to_admin(message, is_critical_error=False):
    if is_critical_error:
        telegram_bot_url = "https://api.telegram.org/bot1603266796:AAGeyFpNbj5z9cOuqaUZd9zCt3lhnSffpEw/sendMessage" \
                           "?chat_id=@easyerrorhandling&text=" + message
    else:
        telegram_bot_url = "https://api.telegram.org/bot1603266796:AAGeyFpNbj5z9cOuqaUZd9zCt3lhnSffpEw/sendMessage" \
                           "?chat_id=@easyaffiliateadmin&text=" + message
    response = requests.post(telegram_bot_url)
    return response


if __name__ == "__main__":
    start_time = time.time()
    while True:
        send_telegram_message_to_admin("WhatsApp Container Restart Job Started..")
        restart_containers()
        send_telegram_message_to_admin("WhatsApp Container Restart Job Completed.")
        if time_interval_seconds is None:
            time_interval_seconds = 43200
        time.sleep(int(time_interval_seconds) - ((time.time() - start_time) % int(time_interval_seconds)))
