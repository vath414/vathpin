from seleniumbase import SB
import json
from function import post

if __name__ == "__main__":
    with SB(uc=True, headless=False) as sb:
        sb.activate_cdp_mode(url="https://www.pinterest.com")

        with open("unused.json", "r") as file:
            cookies = json.load(file)

        for cookie in cookies:
            cookie.pop("sameSite", None)
            cookie.pop("expiry", None)
            sb.add_cookie(cookie)

        sb.open("https://www.pinterest.com/pin-creation-tool/")
        sb.sleep(20)
        post(sb)
