from seleniumbase import Driver
import json
from time import sleep
import os 
from upload_log import upload
import time
from selenium.webdriver.common.by import By
VIDEOS_FOLDER = "video"
url="https://mayarecipes.netlify.app/"


def setup():
    driver=Driver(uc=True)
    driver.get("https://www.pinterest.com")
    with open("cookie.json","r") as file:
        cookies=json.load(file)
    for cookie in cookies:
        cookie.pop("sameSite", None)
        cookie.pop("expiry", None)
        driver.add_cookie(cookie)
    driver.get("https://www.pinterest.com")
    driver.get("https://www.pinterest.com/pin-creation-tool/")
    driver.sleep(20)
    return driver
def check():
    videos = sorted(os.listdir(VIDEOS_FOLDER))
    videos = [v for v in videos if v.endswith(".mp4")]
    for video in videos:
        if video in upload:
            print(f"Skipping already uploaded video: {video}")
        else:
            upload.append(video)
            with open("upload_log.py", "w") as f:
                f.write(f"upload = {upload}\n")
            return video
    print("All are upload")
    return None
def post(driver):
    video=check()
    if video is None:
        driver.quit()
        return
    title=video.replace("_","").replace(".mp4","")
    file_path = os.path.abspath(os.path.join(VIDEOS_FOLDER, video))
    driver.find_element(By.CSS_SELECTOR,"#storyboard-upload-input").send_keys(file_path)
    time.sleep(3)
    try:
        driver.click("#storyboard-selector-title")
        driver.update_text("#storyboard-selector-title", title)
    except:
        print("cant find title field")
    try:
        driver.type("div[contenteditable='true']","credit to the onwer")
    except:
        print("cant find credit field")
    try:
        driver.type("#WebsiteField",url)
    except:
        print("cant find website field")

    driver.click("xpath=//button[.//div[text()='Publish']]")
    driver.sleep(20)
    driver.quit()




