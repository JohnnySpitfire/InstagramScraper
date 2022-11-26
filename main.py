"""_summary_
"""
from glob import glob
from tkinter import W
import requests as req
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as Ex
import time
from pynput.keyboard import Key, Listener

IS_COMPLETED = False
    
def on_press(key):
    """_summary_

    Args:
        key (_type_): _description_
    """
    if key == Key.num_lock:
        global IS_COMPLETED
        IS_COMPLETED = True

def write_html(driver):
    """_summary_

    Args:
        driver (WebDriver): Selenium Webdriver.
    """
    file = open("source.html", "w", encoding="utf-8")
    html = driver.page_source.encode("utf-8")
    file.write(str(html))
    file.close()
    
def wait_for_response(driver, type, value):
    """Awaits for a value to become avalible on the DOM.

    Args:
        driver (WebDriver): Selenium WebDriver.
        type (String): Type of search to perform on the DOM.
        value (String): Value to search for.
    """
    match type:
        case "ID":
            try:
                wait = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, value))
                )
            except:
                pass
        case "XPATH_VALUE":
            try:
                wait = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), \"{value}\")]")))
            except:
                pass
        case "XPATH_CLASS":
            try:
                wait = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@class=\"{value}\"]")))
            except:
                pass
        case "TAG_NAME":
            try:
                wait = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, value))
                )
            except:
                pass

def login(driver):
    """_summary_

    Args:
        driver (WebDriver): Selenium WebDriver
    """
    print("Logging In....")
    driver.get("https://www.instagram.com/direct/t/340282366841710300949128299951790614236/")
    wait_for_response(driver, "ID", "loginForm")
    login_form = driver.find_element(By.TAG_NAME, "form")
    login_form.find_element(By.NAME, "username").send_keys("ben_john555")
    login_form.find_element(By.NAME, "password").send_keys("1Spitfire1")
    login_form.submit()
    try:
        wait = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), \"Not Now\")]"))
        )
    except:
        raise Ex.ElementNotInteractableException    
    not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), \"Not Now\")]")
    not_now_btn.click()
    write_html(driver)
    try:
        wait = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), \"Not Now\")]"))
        )
    except:
        raise Ex.ElementNotInteractableException
    not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), \"Not Now\")]")
    not_now_btn.click()
    wait_for_response(driver, "XPATH_VALUE", "Masters of Spinjitzu")
    message_box = driver.find_element(By.XPATH, "//div[@class=\"xdt5ytf x78zum5\"]")
    message_box.click()
    print("Logged In!")
    
def load_messages(driver, actions):
    global IS_COMPLETED
    print("Loading Messages....")
    while IS_COMPLETED is False:
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
    messages = driver.find_elements(By.XPATH, "//div[@class=\"_ab8w  _ab94 _ab96 _ab9f _ab9k _ab9p _abcm\"]")
    usernames = driver.find_elements(By.XPATH, "//div[@class=\"_ab8w  _ab94 _ab96 _ab9f _ab9k _ab9p _abcm\"]//preceding-sibling::div[@class = \"_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p _abcm\"][1]")
    usernames_messages = list(zip(messages, usernames))
    print("Messages Found!")
    audio_messages = []
    image_messages = []
    text_messages = []
    i = 0
    while i < len(usernames_messages):
        try:
            usernames_messages[i][0].find_element(By.TAG_NAME, "audio")
        except Ex.NoSuchElementException:
            try:
                usernames_messages[i][0].find_element(By.XPATH, "//div[@class=\"_aacl _aaco _aacu _aacx _aad6 _aade\"]")
            except Ex.NoSuchElementException:
                try:
                    usernames_messages[i][0].find_element(By.XPATH, "//img[not(@class)]")
                except Ex.NoSuchElementException:
                    pass
                else:
                    image_messages.append(usernames_messages[i])
                    i += 1
            else:
                text_messages.append(usernames_messages[i])
                i += 1
        else:
            audio_messages.append(usernames_messages[i])
            i += 1
    extract_voice_messages(audio_messages)

def extract_voice_messages(voice_messages):
    i = 0
    username_occourences = {}
    for message in voice_messages:
        i += 1
        audio_src = message[0].find_element(By.TAG_NAME, "source").get_dom_attribute("src")
        try:
            username_element = message[0].find_element(By.XPATH, "//div[@class=\"_ab8w  _ab94 _ab96 _ab9g _ab9k _ab9p _abcm\"]")
            # username_element = message.find_element(By.XPATH, "//preceding-sibling::div[@class = \"_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p _abcm\"]")
            username = username_element.find_element(By.TAG_NAME, "a").get_dom_attribute("href")[1:-1]
        except:
            username_element = message[1]
            username = username_element.find_element(By.XPATH, "//div[@class=\"_aacl _aacn _aacu _aacy _aada\"]").text
        if username not in username_occourences.keys():
            username_occourences[username] = 1
        else:
            username_occourences[username] += 1
        audio_file = req.get(audio_src)
        file_name = f"{i}_{username}_{username_occourences[username]}"
        print(f"downloading {file_name}.mp3")
        with open(f"audio/{file_name}.mp3", "wb") as f:
            f.write(audio_file.content)
            
def extract_text_messages(driver):
    i = 0
    username_element = driver.find_element(By.XPATH, "//div[@class=\"_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _abak _abbi _abcm\"]")
    username = username_element.find_element(By.TAG_NAME, "a").get_dom_attribute("href")[1:-1]

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    actions = ActionChains(driver)
    listener = Listener(on_press=on_press)
    listener.start()
    login(driver)
    load_messages(driver, actions)
    get_messages(driver)
    driver.quit()
