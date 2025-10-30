from seleniumbase import SB
import json
import os
import time
from upload_log import upload
import random
import csv
import requests

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

    # for i in range(3):
    #     try:
    #         sb.clear("#combobox-storyboard-interest-tags")
    #         sb.type("#combobox-storyboard-interest-tags", get_tag())
    #         sb.sleep(5)
    #         suggestion=sb.cdp.find_all("div[data-test-id='storyboard-suggestions-item']")
    #         print(suggestion[1])
    #         try:
    #             sb.cdp.gui_click_element(suggestion[1])
    #             print("✓ Tag set")
    #         except:
    #             print(f"could not find tag: {get_tag()}")
    #     except Exception as e:
    #         print(e)
    try:
        sb.wait_for_element("//div[contains(text(),'Publish')]", timeout=10)
        sb.highlight("//div[contains(text(),'Publish')]")
        position=sb.cdp.get_element_position("//div[contains(text(),'Publish')]", timeout=None)
        time.sleep(1)
        sb.cdp.gui_click_x_y(1250,250 , timeframe=0.25)
        print(position)
        print("✓ GUI clicked Publish button")
        sb.sleep(30)
        print("Process completed")
    except Exception as e:
        print(f"Failed to click publish button: {e}")
        return
def save_pin(sb):
    sb.get("https://www.pinterest.com/MayaRecipes112/burgers-sandwiches/_tools/more-ideas/?ideas_referrer=23")
    time.sleep(3)
    print("go to link burger")
    time.sleep(1)
    try: 
        save_buttons = sb.find_elements("svg[aria-label='Save']")
        for button in save_buttons:
            sb.click(button)
    except Exception as e:
        print(e)
def scrape(sb):
    sb.get("https://www.pinterest.com/mytastedz/_created/")
    sb.sleep(5)

    # --- Scroll to load all pins ---
    print("🔄 Scrolling to load pins...")
    previous_count = 0
    scroll_pause = 2

    for _ in range(30):  # scroll up to 30 times (adjust if needed)
        sb.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sb.sleep(scroll_pause)
        pins = sb.find_elements("//a[contains(@href, '/pin/')]")
        if len(pins) == previous_count:
            break
        previous_count = len(pins)

    print(f"✅ Total pins loaded: {len(pins)}")

    # --- Scrape data ---
    data = []
    for pin in pins:
        try:
            # Open pin in a new tab
            href = sb.get_attribute(pin, "href")
            if not href.startswith("http"):
                href = "https://www.pinterest.com" + href

            sb.driver.execute_script(f"window.open('{href}', '_blank');")
            sb.switch_to_window(sb.driver.window_handles[-1])
            sb.sleep(3)

            # Image
            try:
                img = sb.get_attribute("//img[contains(@src, 'pinimg.com')]", "src")
            except:
                img = ""

            # Title
            try:
                title = sb.get_text("//h1")
            except:
                title = ""

            # Description
            try:
                desc = sb.get_text("//div[contains(@data-test-id, 'PinDescription')]")
            except:
                desc = ""

            if img:
                data.append({"image": img, "title": title, "description": desc})
                print(f"📌 Scraped: {title[:40]}")

            # Close pin tab and return
            sb.driver.close()
            sb.switch_to_window(sb.driver.window_handles[0])

        except Exception as e:
            print("❌ Error:", e)
            sb.switch_to_window(sb.driver.window_handles[0])

    # --- Save results to CSV ---
    with open("pinterest_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["image", "title", "description"])
        writer.writeheader()
        writer.writerows(data)

    print(f"\n✅ Scraping complete! {len(data)} items saved to pinterest_data.csv")

    # --- Optional: download images ---
    os.makedirs("downloaded_images", exist_ok=True)
    for i, item in enumerate(data):
        try:
            img_data = requests.get(item["image"]).content
            file_path = f"downloaded_images/pin_{i+1}.jpg"
            with open(file_path, "wb") as f:
                f.write(img_data)
        except:
            pass

    print("🖼️ Images saved in 'downloaded_images' folder.")
    sb.quit()
