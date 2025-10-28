from seleniumbase import Driver
import json
import os
import time
from upload_log import upload
import random

VIDEOS_FOLDER = "video"
decs="Credit to the onwer"
url="https://www.pinterest.com"
def setup():
    with Driver(uc=True) as sb:
        url = "https://www.pinterest.com"
        sb.get(url)
        with open("unused.json", "r") as file:
            cookies = json.load(file)

        for cookie in cookies:
            cookie.pop("sameSite", None)
            cookie.pop("expiry", None)
            sb.add_cookie(cookie)

        # Navigate to upload page
        sb.open("https://www.pinterest.com/pin-creation-tool/")
        sb.sleep(20)
        return sb
def get_tag():
    with open("tag.txt","r") as f:
        tag=f.readlines()
    tag=random.choice(tag)
    return tag
def check():
    """Get next video to upload. Return None if all uploaded."""
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
    return None

def post(driver):
    video = check()
    if video is None:
        print("All videos are posted")
        driver.quit()
        return
    
    title = video.replace("_", " ").replace(".mp4", "")
    file_path = os.path.abspath(os.path.join(VIDEOS_FOLDER, video))
    
    print(f"Starting upload for: {video}")
    
    # Upload video
    driver.find_element("#storyboard-upload-input").send_keys(file_path)
    print("✓ Video file selected")
    time.sleep(3)
    
    # Set title
    try:
        driver.type("#storyboard-selector-title",title)
        print("✓ Title set")
        time.sleep(1)
    except Exception as e:
        print(e)

    # fill url
    try:
        driver.type("//input[@id='WebsiteField']", "https://www.mayarecipes.netlify.app")
        print("✓ Set url")
        time.sleep(1)
    except Exception as e:
        print("fail url")
    
    # add tags
    for i in range(3):
        try:
            driver.find_element("#combobox-storyboard-interest-tags").clear()
            driver.type(f"#combobox-storyboard-interest-tags",{get_tag()})
            driver.sleep(5)
            try:
                driver.click("(//span[@role='option'])[1]")
                time.sleep(1)
                print("✓ Tag set")
            except Exception as e:
                print(f"couldnot find tag: {get_tag()}")
        except Exception as e:
            print(e)

    #publish
    try:
        driver.click("//button[.//div[contains(text(), 'Publish')]]")
        time.sleep(30)
        print("Process completed")
    except Exception as e:
        print(f"Failed to click publish button: {e}")
        driver.quit()
        return
    # Final wait and cleanup
    driver.quit()