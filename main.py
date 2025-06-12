import os
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from prompt import Prompt

load_dotenv()  # Load from .env file

phone_number = os.getenv("PHONE_NUMBER")

class TinderAgent():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)
        self.prompt = Prompt()

    def login(self):
        self.driver.get("https://www.tinder.com")

        time.sleep(3)

        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log in')]")))
        login_button.click()

        time.sleep(3)
        try:
            accept_cookies = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'I accept')]")))
            accept_cookies .click()
        except:
            print("no cookies")

        phone_login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Log in with phone number']")))
        phone_login_button.click()

        phone_number_input = self.wait.until(EC.presence_of_element_located((By.ID, "phone_number")))
        phone_number_input.send_keys(phone_number)
        phone_number_input.send_keys(Keys.RETURN)
        print("Phone number entered check for text code and email code")

        input("AFTER you finish login (and are inside Tinder), press Enter to continue...")

        try:
            allow_location = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Allow')]")))
            allow_location.click()
        except:
            print("ask to allow location")

        try:
            miss_notifications = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'I’ll give it a miss')]")))
            miss_notifications.click()
        except:
            print("no catch")

        time.sleep(2)

    def reject_add_to_homescreen(self):
        try:
        # reject pop up for add to home screen
            not_interested_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Not interested')]"))
            )
            not_interested_button.click()
            print("Clicked 'Not interested' button")
        except Exception as e:
            print(f"Failed to click 'Not interested' button: {e}")

    def swipe_right(self):
        swipe_right = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Like']]")))
        swipe_right.click()

    def swipe_left(self):
        swipe_left = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Nope']]")))
        # swipe_left.click()

    def auto_swiper(self):
        time.sleep(1)
        self.maybe_later()
        while True:
            time.sleep(0.2)
            print("sleep before swipe")
            try:
                self.swipe_right()
                print("swiping right")

                if self.is_match_popup():
                    self.handle_match_popup()
                    continue
                self.reject_add_to_homescreen()
                self.get_matches()
                # self.close_offer()
            except Exception as e:
                print(f"failed to swipe right: {e}")

                try:
                    # self.swipe_left()
                    print("hitting swipe left")
                    self.reject_add_to_homescreen()
                except Exception as e:
                    print(f"failed to swipe left: {e}")
                    break

        print("selected not to add to home screen")

        input("Press Enter to close the browser...")

        self.driver.quit()

    def close_offer(self):
        print("trying to close offer")
        try:
        # close the offer if you get one
            close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Close']]")))
            close_button.click()
            print("closing offer can no longer continue")
            sys.exit(1)
        except Exception as e:
            print(f"Failed to close offer or was no offer: {e}")

    def is_match_popup(self):
        try:
            match_popup = self.driver.find_element(By.XPATH, "//div[contains(text(), \"It's a Match!\")]")
            return match_popup.is_displayed()
        except:
            return False
        
    def handle_match_popup(self):
        print("Handling match popup...")
        
        try:
            # Try clicking “Keep Swiping” or “Send a Message”
            keep_swiping_btn = self.driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Keep Swiping')]]")
            keep_swiping_btn.click()
            print("Clicked Keep Swiping")
        except Exception as e:
            print(f"Could not handle match popup: {e}")

            

    def get_matches(self):
        print("attempting to write prompt to match")
        try:
            new_match_msg = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//textarea[@placeholder='Say something nice!']")
            ))
            random_prompt = self.prompt.get_random_prompt()
            new_match_msg.send_keys(random_prompt)
            new_match_msg.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"couldnt send a message: {e}")

    def maybe_later(self):
        print("trying to click maybe later for matches that like you")
        try:
            maybe_later = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//button[.//div[normalize-space(text())='Maybe later']]")
            ))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//div[normalize-space(text())='Maybe later']]")))
            maybe_later.click()
        except Exception as e:
            print(f"maybe later not clicked: {e}")


def main():
    agent = TinderAgent()
    agent.login()
    agent.auto_swiper()

if __name__ == "__main__":
    main()
