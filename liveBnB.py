from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


# Connecting to Browser
options = webdriver.ChromeOptions()
user_data_path = r'C:\Users\talha\AppData\Local\Google\Chrome\User Data'
options.add_argument(f'user-data-dir={user_data_path}')
# Chrome ID
profile_directory = 'Profile 2'
options.add_argument(f'--profile-directory={profile_directory}')
driver = webdriver.Chrome(options=options)
driver.get("https://www.binance.com/en/live")
driver.execute_script("window.scrollBy(0, 250);")

# Wait for a bit on the live page
time.sleep(5)

# finding categories on binance live
category = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//a[@href='/en/live/category/7']"))
)
# Below line will scroll to the above element
ActionChains(driver).move_to_element(category).perform()
category.click()

main_window_handle = driver.current_window_handle

# Variables
data = []
processedProfiles = set()

# Program to convert followers from text to Number


def convert_followers_to_int(followers_text):
    multiplier = 1
    if 'k' in followers_text:
        multiplier = 1000
        followers_text = followers_text.replace('k', '')
    elif 'm' in followers_text:
        multiplier = 1000000
        followers_text = followers_text.replace('m', '')
    # Remove any commas or dots
    followers_text = followers_text.replace(',', '')
    followers_count = float(followers_text) * multiplier
    return int(followers_count)


def getStreamerData():
    last_height = driver.execute_script("return document.body.scrollHeight")
    max_scrolls = 60
    scrolls_count = 0
    while scrolls_count < max_scrolls:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load
        time.sleep(6)

        # Finding the streamers
        cards = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'cardlist-live-user')))

        for card in cards:
            profile_links = card.find_elements(By.TAG_NAME, 'a')
            if len(profile_links) > 1:
                profile_url = profile_links[1].get_attribute('href')

                # Check if this profile URL is the same as the last opened one
                if profile_url in processedProfiles:
                    print("Skipping the same profile")
                    continue  # Skip this iteration and don't open the same profile again.

                # If its unique below line will add it to the set.
                processedProfiles.add(profile_url)
                # Click the second 'a' tag to open the profile
                profile_links[1].click()
                time.sleep(5)
                # Wait for the new tab to open and switch to it
                new_tab_handle = [
                    handle for handle in driver.window_handles if handle != main_window_handle][0]
                driver.switch_to.window(new_tab_handle)

                # Scrape the required data from the streamer's profile
                # Assuming you have the correct selectors for ID, followers and bio.

                profile_id = driver.find_element(
                    By.CLASS_NAME, "css-1krd9w6").text

                # Using the find elements because followers and following has the same class.
                followers_text = driver.find_elements(
                    By.CLASS_NAME, "value.css-vurnku")[1].text
                # Converting followers to numbers
                followers_count = convert_followers_to_int(followers_text)

                # Trying to find Bio
                try:
                    # Attempt to find the bio element
                    bio = driver.find_element(
                        By.CLASS_NAME, "css-8uczs3").text
                except NoSuchElementException:
                    # If the bio element is not found, set bio_text to None or an empty string
                    bio = 'No Bio'

                # Checking if ID is verified or Not
                try:
                    driver.find_element(By.CLASS_NAME, "css-1e3vi3w")
                    is_verified = True
                except NoSuchElementException:
                    is_verified = False

                if is_verified:
                    verified = "Yes"
                else:
                    verified = "No"

                if followers_count >= 20000:
                    # Append the data to the list
                    data.append({'ID': profile_id, 'BnbLive Link': profile_url,
                                'Followers': followers_count, 'Bio': bio, 'Verified': verified})
                    print(f"Data appending for {profile_id}")
                    print(pd.DataFrame(data))

                # Close the new tab and switch back to the main window
                driver.close()
                driver.switch_to.window(main_window_handle)

                # Wait before moving to the next streamer link to avoid quick, bot-like behavior
                print(f"Waiting before next streamer")
                time.sleep(5)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height > last_height:
                    # increasing the scroll count
                    scrolls_count += 1
                    print(f"Scroll count is {scrolls_count}")
                    last_height = new_height
                    # If new height is either lesser or equal below statement will execute.
                else:
                    print("No new content to scroll to.")
                    break    
        # Checking if there is new data if it is print and append to sheet. 
        if data:
            print(f"Reached {scrolls_count}")
            df = pd.DataFrame(data)
            df.to_excel('streamers_data.xlsx', index=False)
            print(f"Data saved to streamers_data.xlsx")
        else:
            print(f"No data collected")


getStreamerData()


# Close the browser after all operations

driver.quit()
