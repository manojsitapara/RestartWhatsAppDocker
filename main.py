import docker
import requests
import time


def send_telegram_message_to_admin(message, is_critical_error=False):
    if is_critical_error:
        telegram_bot_url = "https://api.telegram.org/bot1183011189:AAH4qHDMUAdcLmVGcLiqrbQXVc3Xqn102-E/sendMessage?chat_id=@easyerrorhandling&text=" + message
    else:
        telegram_bot_url = "https://api.telegram.org/bot1183011189:AAH4qHDMUAdcLmVGcLiqrbQXVc3Xqn102-E/sendMessage?chat_id=@AffiliateJobNotification&text=" + message
    response = requests.post(telegram_bot_url)
    return response


if __name__ == "__main__":
    start_time = time.time()
    while True:
        send_telegram_message_to_admin("WhatsApp Container Restart Job Started..")
        client = docker.from_env()
        container_results = client.containers.list()
        for container in container_results:
            container.restart()
            send_telegram_message_to_admin("WhatsApp container - {} is restarted".format(container.name))
        send_telegram_message_to_admin("WhatsApp Container Restart Job Completed.")
        time.sleep(10000.0 - ((time.time() - start_time) % 10000.0))