from seleniumbase import SB
import json
import os
import time
from upload_log import upload
import random

VIDEOS_FOLDER = "video"
desc = "Credit to the owner"
url = "https://www.pinterest.com"

def get_tag():
    with open("tag.txt","r") as f:
        tag = f.readlines()
    return random.choice(tag).strip()

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
    return None

def post(sb):
    video = check()
    if video is None:
        print("All videos are posted")
        return

    title = video.replace("_", " ").replace(".mp4", "")
    file_path = os.path.abspath(os.path.join(VIDEOS_FOLDER, video))
    print(f"Starting upload for: {video}")

    sb.choose_file("#storyboard-upload-input", file_path)
    print("✓ Video file selected")
    time.sleep(3)

    try:
        sb.type("#storyboard-selector-title", title)
        print("✓ Title set")
        time.sleep(1)
    except Exception as e:
        print(e)

    try:
        sb.type("#WebsiteField", "https://www.mayarecipes.netlify.app")
        print("✓ Set URL")
        time.sleep(1)
    except Exception as e:
        print("fail url")

    for i in range(3):
        try:
            sb.clear("#combobox-storyboard-interest-tags")
            sb.type("#combobox-storyboard-interest-tags", get_tag())
            sb.sleep(5)
            suggestion=sb.cdp.find_all("div[data-test-id='storyboard-suggestions-item']")
            try:
                sb.click(suggestion[0])
                print("✓ Tag set")
            except:
                print(f"could not find tag: {get_tag()}")
        except Exception as e:
            print(e)
    try:
        sb.wait_for_element("//div[contains(text(),'Publish')]", timeout=10)
        sb.highlight("//div[contains(text(),'Publish')]")
        sb.cdp.gui_click_element("//div[contains(text(),'Publish')]")
        print("✓ GUI clicked Publish button")
        sb.sleep(30)
        print("Process completed")
    except Exception as e:
        print(f"Failed to click publish button: {e}")
        return
