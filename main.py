"""_summary_
"""
import requests as req
import threading
import sys
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as Ex
import time
from pynput.keyboard import Key, Listener

LOADING_MESSAGES = False
LOADING_ANIMATION_ACTIVE = True
LOGGING_IN = False

def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '*', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'{prefix} |{bar}| {percent}% {suffix}', end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()
        
# def loading_animation():
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if LOADING_ANIMATION_ACTIVE:
#             if LOGGING_IN:
#                 sys.stdout.write('\rLogging In...' + c)
#                 sys.stdout.flush()
#                 time.sleep(0.1)
#             if LOADING_MESSAGES:
#                 sys.stdout.write('\rLoading Messages..' + c)
#                 sys.stdout.flush()
#                 time.sleep(0.1)
            
def on_press(key):
    """_summary_

    Args:
        key (_type_): _description_
    """
    if key == Key.num_lock:
        global LOADING_MESSAGES, LOADING_ANIMATION_ACTIVE
        LOADING_MESSAGES, LOADING_ANIMATION_ACTIVE = False, False

def write_html(driver):
    """_summary_

    Args:
        driver (WebDriver): Selenium Webdriver.
    """
    file = open("source.html", "w", encoding="utf-8")
    html = driver.page_source.encode("utf-8")
    file.write(str(html))
    file.close()
    
def wait_for_response(driver, type, value, timeout=30):
    """Awaits for a value to become avalible on the DOM.

    Args:
        driver (WebDriver): Selenium WebDriver.
        type (String): Type of search to perform on the DOM.
        value (String): Value to search for.
    """
    match type:
        case "ID":
            try:
                wait = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.ID, value))
                )
            except:
                pass
        case "XPATH_VALUE":
            try:
                wait = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), \"{value}\")]")))
            except:
                pass
        case "XPATH_CLASS":
            try:
                wait = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@class=\"{value}\"]")))
            except:
                pass
        case "TAG_NAME":
            try:
                wait = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME, value))
                )
            except:
                pass

def login(driver):
    """_summary_

    Args:
        driver (WebDriver): Selenium WebDriver
    """
    global LOGGING_IN, LOADING_ANIMATION_ACTIVE
    LOGGING_IN, LOADING_ANIMATION_ACTIVE = True, True
    print("Logging In....")
    driver.get("https://www.instagram.com/direct/t/340282366841710300949128299951790614236/")
    wait_for_response(driver, "ID", "loginForm")
    login_form = driver.find_element(By.TAG_NAME, "form")
    login_form.find_element(By.NAME, "username").send_keys("ben_john555")
    login_form.find_element(By.NAME, "password").send_keys("1Spitfire1")
    login_form.submit()
    clear_notification_popups(driver)
    LOGGING_IN, LOADING_ANIMATION_ACTIVE = False, False
    print("Logged In!")

def clear_notification_popups(driver):
    try:
        wait = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), \"Not Now\")]"))
        )
    except:
        raise Ex.ElementNotInteractableException    
    not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), \"Not Now\")]")
    not_now_btn.click()
    write_html(driver)
    try:
        wait = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), \"Not Now\")]"))
        )
    except:
        # raise Ex.ElementNotInteractableException
        pass
    not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), \"Not Now\")]")
    not_now_btn.click()
    wait_for_response(driver, "XPATH_VALUE", "Masters of Spinjitzu", 5)
    # message_box = driver.find_element(By.XPATH, "//div[@class=\"_ab5z _ab5_\"]")
    # message_box.click()
    
def load_messages(driver, actions):
    global LOADING_MESSAGES, LOADING_ANIMATION_ACTIVE
    LOADING_MESSAGES, LOADING_ANIMATION_ACTIVE = True, True
    print("Loading Messages....")
    while LOADING_MESSAGES is True:
        wait_for_response(driver, "XPATH_CLASS", "_aacl _aacn _aacu _aacy _aada")
        try:
            message_box = driver.find_element(By.XPATH, "//div[@class=\"_aacl _aacn _aacu _aacy _aada\"]")
            message_box.click()
        except:
            time.sleep(60)
            message_box = driver.find_element(By.XPATH, "//div[@class=\"_aacl _aacn _aacu _aacy _aada\"]")
            message_box.click()
        actions.send_keys(Keys.CONTROL, Keys.HOME)
        try:
            wait = WebDriverWait(driver,1000).until_not(
                EC.presence_of_element_located((By.XPATH, "//svg[@class=\"_abdx\"]"))
            )
        except:
            pass
    print("Finished Loading!")
        
def get_messages(driver):
    print("Getting Messages....")
    box = driver.find_element(By.XPATH, "//div[@class=\"_ab5z _ab5_\"]/div")
    messages_and_usernames = box.find_elements(By.XPATH, "./div[@class=\"_ab8w  _ab94 _ab96 _ab9f _ab9k _ab9p _abcm\"] | ./div[@class=\"_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p _abcm\"]")
    message_dict = {}
    line_count = len(messages_and_usernames)
    for index, line in enumerate(messages_and_usernames):
        if "AM" in line.text or "PM" in line.text:
            messages_and_usernames.remove(line)
        print_progress_bar(index, line_count, "Removing Redundant Elements:", f"{line_count - len(messages_and_usernames)} lines removed")
    i = len(messages_and_usernames) - 1
    while i >= 0:
        name_found = False
        username = ""
        print_progress_bar(len(messages_and_usernames) -i, len(messages_and_usernames), "Collecting Messages:", "Collected")
        if messages_and_usernames[i].get_dom_attribute("class") == "_ab8w  _ab94 _ab96 _ab9f _ab9k _ab9p _abcm":
            j = i
            while name_found == False and j >= 0:
                try:
                    if messages_and_usernames[j].get_dom_attribute("class") == "_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p _abcm":
                        name_found = True
                        username = messages_and_usernames[j].text
                        if username == '':
                            username = "ben_john555"
                        if username not in message_dict:
                            message_dict[username] = [messages_and_usernames[i]]
                        else:
                            message_dict[username].append(messages_and_usernames[i])
                except:
                    print(Ex.StaleElementReferenceException)
                else:
                    j -= 1
        i -= 1
    print("Messages Found!")
    audio_messages = []
    image_messages = []
    text_messages = []
    for user in message_dict:
        i = 0
        while i < len(message_dict[user]):
            print_progress_bar(i, len(message_dict[user]), f"Categorizing {user}'s Messages", "Completed")
            try:
                message_dict[user][i].find_element(By.TAG_NAME, "audio")
            except Ex.NoSuchElementException:
                try:
                    message_dict[user][i].find_element(By.XPATH, "//div[@class=\"_aacl _aaco _aacu _aacx _aad6 _aade\"]")
                except Ex.NoSuchElementException:
                    try:
                        message_dict[user][i].find_element(By.XPATH, "//img[not(@class)]")
                    except Ex.NoSuchElementException:
                        raise Exception("Unexpected Element Type")
                    else:
                        image_messages.append((user, message_dict[user][i]))
                        i += 1
                else:
                    text_messages.append((user, message_dict[user][i]))
                    i += 1
            else:
                audio_messages.append((user, message_dict[user][i]))
                i += 1
                
    download_voice_messages(audio_messages)
    download_images(image_messages)
    process_text_messages(text_messages, audio_messages)
    
    print_user_stats(message_dict, audio_messages)

def print_user_stats(message_dict, audio_messages):
    for user in message_dict:
        audio_message_count = 0
        for username, message in audio_messages:
            if username == user:
                audio_message_count += 1
        print(f"{user}'s Total Number of Messages: {message_dict[user].count()}")
        print(f"{user}'s Total Number of Audio Messages: {audio_message_count}")
    
def process_text_messages(text_messages):
    i = 0
    with open("text_messages.csv", "xt") as f:        
        for username, message in text_messages:
            print_progress_bar(i, len(text_messages), "Processing Text Messages:", "Processed")
            f.write(f"{username},{message.text}")

def download_images(image_messages):
    i = 0
    for username, message in image_messages:
        print_progress_bar(i, len(image_messages), "Downloading Images:", "Downloaded")
        i += 1
        img_src = message.get_dom_attribute("src")
        image_file = req.get(img_src)
        file_name = f"{i}_{username}"
        with open(f"img/{file_name}.jpg", "wb") as f:
            f.write(image_file.content)

def download_voice_messages(voice_messages):
    i = 0
    for username, message in voice_messages:
        print_progress_bar(i, len(voice_messages), "Downloading Messages:", "Downloaded")
        i += 1
        audio_src = message.find_element(By.TAG_NAME, "source").get_dom_attribute("src")
        audio_file = req.get(audio_src)
        file_name = f"{i}_{username}"
        with open(f"audio/{file_name}.mp3", "wb") as f:
            f.write(audio_file.content)

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    # t = threading.Thread(target=loading_animation)
    # t.start()
    actions = ActionChains(driver)
    listener = Listener(on_press=on_press)
    listener.start()
    login(driver)
    load_messages(driver, actions)
    get_messages(driver)
    driver.quit()
