import random

async def apply_stealth(page):
    """
    Applies common stealth patches to the playwright page.
    Note: In a full production env, we'd use playwright-stealth package,
    but we implement core overrides here for direct control.
    """
    
    # 1. Mask WebDriver
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    
    # 2. Mock Plugins
    await page.add_init_script("""
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                { name: 'Chrome PDF Viewer', filename: 'internal-pdf-viewer' },
                { name: 'Chromium PDF Viewer', filename: 'internal-pdf-viewer' }
            ]
        });
    """)

    # 3. Handle Chrome Runtime
    await page.add_init_script("""
        window.chrome = {
            runtime: {}
        };
    """)

    # 4. Consistent Languages and Viewport
    # (Handled via context creation in session_manager, but reinforced here)
    await page.add_init_script("""
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
    """)

def get_random_ua():
    """Returns a realistic modern user agent."""
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    return random.choice(uas)
