from playwright.sync_api import sync_playwright, Browser, Page

def get_browser_and_page(headless: bool = True) -> tuple[Browser, Page]:
    """
    Bot tespit mekanizmalarını azaltan konfigürasyonla 
    bir Chromium instance'ı ve sayfa döndürür.
    """
    p = sync_playwright().start()
    
    browser = p.chromium.launch(
        headless=headless,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )
    
    context = browser.new_context(
        viewport={"width": 1366, "height": 768},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        locale="az-AZ"
    )
    
    page = context.new_page()
    
    # webdriver özelliğini gizle
    page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver")
    
    return browser, page