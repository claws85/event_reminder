# encoding=utf8
#!/usr/bin/python3

import datetime
import logging
import requests

from config import DATES, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(filename='event_reminder.log', level=logging.INFO)

telegram_url = 'https://api.telegram.org/bot{}/'.format(TELEGRAM_BOT_TOKEN)

time_delta = 14

message_template = "The following event(s) will occur {} days from today!\n{}"


def main():
    today = datetime.date.today()
    event_list = ''
    event_template = '\n{}: on {} \nAddress: {}\n'
    try:
        for k, v in DATES.items():
            if future_date(today, time_delta) == k:
                new_event = event_template.format(v.get('event'), k, v.get('address'))
                event_list = event_list + new_event

        if event_list:
            # call method to send notifications
            status = send_text(message_template.format(time_delta, event_list))

            dt = datetime.datetime.now().strftime("%x %X")
            if status == 200:
                logging.info(
                    "Text sent to group successfully at {}.\n".format(dt)
                )
            if str(status).startswith('4'):
                logging.error(
                    "Error detected when sending message at {}."
                    "Status code {}.\n".format(dt, status)
                )

    except Exception as e:
        dt = datetime.datetime.now().strftime("%x %X")
        logging.error(
            "The following error was encountered at {}:"
            "\n{}".format(dt, e)
        )
        send_text(
            "An exception was encountered during the running of the "
            "event_reminder app. Check the logs :)"
        )


def send_text(text):
    """Sends some text via a bot to the chosen group. Returns
    the request status_code for validating"""
    url = telegram_url + 'sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID,
            'text': text}
    r = requests.post(url, data=data)

    return r.status_code


def future_date(date_today, day_delta):
    """Returns future isoformat date (date today + day_delta)
    in string form"""
    fut_date = date_today + datetime.timedelta(days=day_delta)
    return fut_date.strftime('%d - %m')


if __name__ == '__main__':
    main()
