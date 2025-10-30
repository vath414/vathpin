from seleniumbase import SB
import json
from function import post,scrape,save_pin

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
        save_pin(sb)
