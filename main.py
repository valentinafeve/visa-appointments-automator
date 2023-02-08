import logging
import os
from seleniumbot import VisaBot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8.8s] %(message)s",
    handlers=[logging.StreamHandler()],
)

email = os.environ['USVISA_EMAIL']
password = os.environ['USVISA_PASSWORD']

visa = VisaBot(email=email, password=password)
visa.search_for_dates()
