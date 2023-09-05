import re
import time

from playwright.sync_api import sync_playwright

class Capcut:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def download(self, script, headless=True, title="output", ratio="16:9"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()

            # Navigate to the Script to video page
            page.goto("https://www.capcut.com/editor-tools/convert-script-to-video")

            # Waits for 3 seconds
            page.wait_for_timeout(3000)

            # Escape Ads
            page.press("body", "Escape")
            page.press("body", "Escape")
            page.press("body", "Escape")
            
            try:
                page.get_by_role("button", name="Sign in").click(timeout=3000)
            except:
                pass
            page.get_by_text("Continue with email").click()
            page.get_by_placeholder("Enter email").fill(self.email)
            page.get_by_placeholder("Enter password").fill(self.password)
            page.get_by_placeholder("Enter password").press("Enter")

            page.locator("#ai-script-generate-editor-wrapper div").first.fill(script)
            page.get_by_text("Generate video").click()
            page.locator("div").filter(has_text=re.compile(fr"^{ratio}$")).nth(1).click()
            page.get_by_text("American Male").click()
            page.get_by_role("option", name="Energetic Male").locator("div").first.click()
            page.get_by_role("dialog").get_by_text("Generate video", exact=True).click()

            page.get_by_text("Export").click()
            page.get_by_placeholder("Enter title of the work").fill(title)
            page.get_by_text("720p").click()
            page.get_by_text("1080p").click()
            page.get_by_role("button", name="Export").click(timeout=120000)
            with page.expect_download() as download_info:
                page.get_by_text("Download").click()
                download = download_info.value
                print(download.path())
                download.save_as(download.suggested_filename)

            browser.close()

if __name__ == "__main__":
    script="""
Hey everyone! 🌙 Want a bedroom that's more than just a place to crash? Make it a relaxation sanctuary!

1️⃣ Color Palette: Choose calming colors like blues or greens. They set a chill vibe.

2️⃣ Scent-scape: Essential oil diffusers or scented candles can totally transform the mood.

3️⃣ Lighting: Soft, warm lighting or dimmers set the perfect chill atmosphere.

4️⃣ Clutter-Free: Keep it neat! A tidy space equals a peaceful mind.

5️⃣ Comfy Essentials: Invest in quality pillows, blankets, and maybe even a weighted blanket for ultimate coziness.

Your bedroom isn't just for sleep; it's your personal retreat. Make it count!
    """
    capcut = Capcut("<Capcut Username", "<Capcut Password>")
    capcut.download(script, ratio="9:16")