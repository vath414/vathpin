from seleniumbase import SB
import json
from function import post,scrape,save_pin
import time

if __name__ == "__main__":
    with SB(uc=True) as sb:
        sb.activate_cdp_mode(url="https://www.pinterest.com")

        with open("unused.json", "r") as file:
            cookies = json.load(file)

        for cookie in cookies:
            cookie.pop("sameSite", None)
            cookie.pop("expiry", None)
            sb.add_cookie(cookie)

        sb.open("https://www.pinterest.com/pin-creation-tool/")
        sb.sleep(5)
        # Move browser to top-left of screen and resize
        #sb.cdp.set_window_rect(x=0, y=0, width=750, height=450)
        sb.get("https://www.pinterest.com/MayaRecipes112/burgers-sandwiches/_tools/more-ideas/?ideas_referrer=23")
        time.sleep(3)
        print("go to link burger")
        time.sleep(1)
        try: 
            sb.cdp.click("svg[aria-label='Save']")
            print("click save")
        except Exception as e:
            print(e)
