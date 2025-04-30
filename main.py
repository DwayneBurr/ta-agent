import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

load_dotenv()  # Load from .env file

api_key = os.getenv("OPENAI_API_KEY")
phone_number = os.getenv("PHONE_NUMBER")

class TinderAgent():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)

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
            print("Didnt ask to allow location")

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
        while True:
            time.sleep(2)
            print("sleep before sswipe")
            try:
                self.swipe_right()
                print("swiping right")
                self.reject_add_to_homescreen()
                self.get_matches()
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

    # def close_match(self):
    #     try:
    #     # close the match if you get one
    #         close_match = self.wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '')]"))
    #         )
    #         close_match.click()
    #         print("closing match to continue swiping")
    #     except Exception as e:
    #         print(f"Failed to close match: {e}")

    def get_matches(self):
        try:
            new_match_msg = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//textarea[@placeholder='Say something nice!']")
            ))
            new_match_msg.send_keys("Hello, nice to meet you!")
            new_match_msg.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"couldnt send a message: {e}")

def main():
    agent = TinderAgent()
    agent.login()
    agent.auto_swiper()

if __name__ == "__main__":
    main()


    # <textarea placeholder="Say something nice!" maxlength="5000" class="P(8px) Fx($flx1) As(c) Typs(body-1-regular) Rsz(n) Px(16px) Py(8px)" id="q237454470" style="height: 40px !important;"></textarea>