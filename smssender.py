import requests
import os


TEXTBELT_API_KEY_NAME = "TEXTBELT_API_KEY"


def get_textbelt_api_key():
  try:
    return os.environ[TEXTBELT_API_KEY_NAME]
  except KeyError:
    raise Exception(f"The environment variable {TEXTBELT_API_KEY_NAME} is not set.")


def send_sms(phone, text, test=True):
  textbelt_api_key = get_textbelt_api_key()
  resp = requests.post('https://textbelt.com/text', data={
    'phone': phone,
    'message': text,
    'key': textbelt_api_key + "_test" if test else '',
  })
  return resp
