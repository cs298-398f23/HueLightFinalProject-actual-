import dotenv
import os
import unittest
from unittest.mock import patch, Mock
from send import send_message, receive_message, find_colors, find_value, SMSReceiver


dotenv.load_dotenv()

AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')

class TestYourFile(unittest.TestCase):

    @patch('twilio.rest.Client')
    @patch('send.RedisHandler')
    def test_send_message(self, mock_twilio_client):
        # Replace the following with appropriate values
        to_phone = 'TO_PHONE_NUMBER'
        text = 'Test message'

        send_message(to_phone, text)
        mock_twilio_client.assert_called_once_with('ACCOUNT_SID', 'AUTH_TOKEN')
        mock_twilio_client.return_value.messages.create.assert_called_once_with(to=to_phone, from_='TWILIO_PHONE', body=text)


    @patch('send.send_message')
    @patch('send.find_colors')
    @patch('send.hueConnect')
    @patch('send.set_current_color')
    def test_receive_message_valid_color(self, mock_set_current_color, mock_hue_connect, mock_find_colors, mock_send_message):
        # Replace the following with appropriate values
        from_number = 'test_number'
        message_text = 'red'

        mock_find_colors.return_value = 'red'
        find_value_return_value = 'red'
        mock_find_colors.return_value = find_value_return_value

        receive_message(from_number, message_text)

        mock_send_message.assert_called_with(from_number, f"Changing light to {message_text} now!")
        mock_hue_connect.assert_called_with(find_value_return_value)
        mock_send_message.assert_called_with(from_number, f"Light successfully changed to {message_text}!")
        mock_set_current_color.assert_called_with(message_text)


    @patch('send.send_message')
    @patch('send.find_colors')
    @patch('send.redis_handler')
    def test_receive_message_invalid_color(self, mock_find_colors, mock_send_message):
        from_number = 'test_number'
        message_text = 'brown'

        mock_find_colors.return_value = None

        receive_message(from_number, message_text)

        mock_send_message.assert_called_with(from_number, f"The color {message_text} is not in the database.")
        mock_send_message.assert_called_with(from_number, f"Please try again with a different color.")


    @patch('send.urllib.parse.parse_qs')
    @patch('send.receive_message')
    def test_sms_receiver_do_get(self, mock_receive_message, mock_parse_qs):
        query_string = 'From=FROM_PHONE_NUMBER&Body=test_message'
        mock_parse_qs.return_value = {'From': ['FROM_PHONE_NUMBER'], 'Body': ['test_message']}
        
        handler = SMSReceiver(Mock(), Mock())
        handler.path = f'/?{query_string}'
        handler.do_GET()

        mock_receive_message.assert_called_once_with('FROM_PHONE_NUMBER', 'test_message')


if __name__ == '__main__':
    unittest.main()