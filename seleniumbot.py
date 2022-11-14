import os
import time

import selenium
import logging
from abc import ABC, abstractmethod
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

EMBASSY_URL = "https://ais.usvisa-info.com/es-co/niv/schedule/38456763/appointment"

MONTHS_RANGE = 80


class VisaBot:
    def __init__(self, email="", password=""):
        self.email = email
        self.password = password

        options = FirefoxOptions()
        options.add_argument("--headless")

        # self.web_driver = webdriver.Firefox(options=options)
        self.web_driver = webdriver.Firefox()
        self.web_driver.get(EMBASSY_URL)
        return

    def select_a_date_given_calendar(self, calendar_picker):
        tries = 0
        while tries < MONTHS_RANGE:
            first_group = calendar_picker.find_element(By.CLASS_NAME, "ui-datepicker-group-first")
            month_name = first_group.find_element(By.CLASS_NAME, "ui-datepicker-month")
            logging.info(f"Looking for dates on {month_name.text}")
            days = first_group.find_elements(By.CSS_SELECTOR, "a.ui-state-default")
            logging.info(f"There are {len(days)} days with availability in month {month_name.text}")

            if days:
                logging.info(f"Selecting a date on {days[0].text} month {month_name.text}")
                days[0].click()
                return True

            second_group = calendar_picker.find_element(By.CLASS_NAME, "ui-datepicker-group-last")
            month_name = second_group.find_element(By.CLASS_NAME, "ui-datepicker-month")
            logging.info(f"Looking for dates on {month_name.text}")
            days = second_group.find_elements(By.CSS_SELECTOR, "a.ui-state-default")
            logging.info(f"There are {len(days)} days with availability in month {month_name.text}")

            if days:
                logging.info(f"Selecting a date on {days[0].text} month {month_name.text}")
                days[0].click()
                return True

            next_button = calendar_picker.find_element(By.CLASS_NAME, "ui-datepicker-next.ui-corner-all")
            next_button.click()
            tries += 2
        return False

    def search_for_hour(self, hour_picker, index_of_hour=-1):
        latest_hour = hour_picker.find_elements(By.TAG_NAME, "option")[index_of_hour]
        latest_hour.click()
        return

    def search_for_dates(self):
        signin_button = self.web_driver.find_element(By.CLASS_NAME, "ui-button.ui-corner-all.ui-widget")
        signin_button.click()
        input_email = self.web_driver.find_element(By.ID, "user_email")
        input_email.send_keys(self.email)
        input_password = self.web_driver.find_element(By.ID, "user_password")
        input_password.send_keys(self.password)

        # Confirming policy
        checkbox = self.web_driver.find_element(By.CLASS_NAME, "icheckbox")
        checkbox.click()

        login_button = self.web_driver.find_element(By.CLASS_NAME, "button.primary")
        login_button.click()

        time.sleep(2)
        # Cita en la Sección Consular
        appointments_dropdown = self.web_driver.find_element(By.ID, "appointments_consulate_appointment_date")
        appointments_dropdown.send_keys(Keys.ENTER)

        calendar_picker = self.web_driver.find_element(By.ID, "ui-datepicker-div")
        date_isselected = self.select_a_date_given_calendar(calendar_picker)

        if not date_isselected:
            logging.info("An available date was not found for the range, quitting...")
            return

        hour_picker = self.web_driver.find_element(By.ID, "appointments_consulate_appointment_time")
        self.search_for_hour(self, hour_picker, index_of_hour=-1)

        # Cita en el CAS
        appointments_dropdown = self.web_driver.find_element(By.ID, "appointments_asc_appointment_date")
        appointments_dropdown.send_keys(Keys.ENTER)

        calendar_picker = self.web_driver.find_element(By.ID, "ui-datepicker-div")
        date_isselected = self.select_a_date_given_calendar(calendar_picker)

        if not date_isselected:
            logging.info("An available date was not found for the range, quitting...")
            return

        hour_picker = self.web_driver.find_element(By.ID, "appointments_asc_appointment_time")
        self.search_for_hour(self, hour_picker, index_of_hour=-1)

        self.web_driver.close()
        return


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8.8s] %(message)s",
    handlers=[logging.StreamHandler()],
)

email = os.environ['USVISA_EMAIL']
password = os.environ['USVISA_PASSWORD']

visa = VisaBot(email=email, password=password)
visa.search_for_dates()