import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError

load_dotenv()

LOGIN_URL = "https://berkayalabalik.myideasoft.com/panel/login"
COOKIE_FILE = Path("ideasoft_storage.json")

EMAIL = os.getenv("IDEASOFT_EMAIL")
PASSWORD = os.getenv("IDEASOFT_PASSWORD")

if not EMAIL or not PASSWORD:
    raise Exception("❌ IDEASOFT_EMAIL veya IDEASOFT_PASSWORD .env içinde yok")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,   # ⚠️ headless yapma, ban riskini artırır
            slow_mo=80
        )

        context = browser.new_context()
        page = context.new_page()

        print("🔐 Ideasoft login sayfası açılıyor...")
        page.goto(LOGIN_URL, timeout=60000)

        # Input selector'ları (Ideasoft standart)
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)

        page.click('button[type="submit"]')

        try:
            # Panel sidebar veya dashboard gelmesini bekle
            page.wait_for_url("**/panel/**", timeout=15000)
            print("✅ Login başarılı!")
        except TimeoutError:
            print("⚠️ Login sonrası panel yüklenemedi")
            print("📍 Mevcut URL:", page.url)
            print("👉 Captcha veya ek doğrulama olabilir")

        # Cookie + localStorage kaydet
        context.storage_state(path=COOKIE_FILE)
        print(f"💾 Cookie kaydedildi → {COOKIE_FILE.resolve()}")

        browser.close()


if __name__ == "__main__":
    main()
