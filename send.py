
import http.server
import urllib.parse
import twilio.rest
import os
import twilio.rest
import redis
from redisUtil import RedisHandler
from huelight import hueConnect
import colorsys
import dotenv

dotenv.load_dotenv()

TWILIO_PHONE = '+18777165114'
token = os.environ.get('AUTH_TOKEN')
account_sid = os.environ.get('ACCOUNT_SID')
twilio_client = twilio.rest.Client(token, account_sid)
redis_handler = RedisHandler()


def send_message(to_phone, text):
    twilio_client.messages.create(to=to_phone, from_=TWILIO_PHONE, body=text)


def receive_message(from_number, message_text):
    print(f'Text message received from {from_number}:{message_text}')
    color = find_colors(message_text)
    # if color in database then send message
    if color is not None:
        response_message = f"Changing light to {message_text} now!"
        send_message(from_number, response_message)
        hueConnect(find_value(message_text))
        response_message = f"Light successfully changed to {message_text}!"
        send_message(from_number, response_message)
    # if color equals "options" then send message
    elif message_text.lower() == "options":
        response_message = f"Please choose from the following colors: red, orange, yellow, green, cyan, blue, purple, pink"
        send_message(from_number, response_message)
    # if color not in database then send message
    else:
        response_message = f"The color {message_text} is not in the database."
        send_message(from_number, response_message)
        response_message = f"Please try again with a different color."
        send_message(from_number, response_message)


def find_colors(text):
    key = text.lower()
    if redis_handler.redis_client.hexists("colors", key):
        return key  # or any value you want to return when the key is "red"
    else:
        color_exists = redis_handler.redis_client.exists(key)
        return color_exists.decode('utf-8') if color_exists else None


def find_value(text):
    key = text.lower()
    if redis_handler.redis_client.hexists("colors", key):
        value = redis_handler.redis_client.hget("colors", key)
        value = value.decode('utf-8') if value else None
        return value


class SMSReceiver(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            qs = urllib.parse.parse_qs(self.path[self.path.index('?')+1:])
            receive_message(qs['From'][0], qs['Body'][0])
        except Exception:
            import sys
            import traceback
            print("Error while processing received text message:", file=sys.stderr)
            traceback.print_exc()
        self.send_response(204)

    def log_message(self, _format, *args):
        return


def main():
    server_address = ('', 8000)
    with http.server.HTTPServer(server_address, SMSReceiver) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
