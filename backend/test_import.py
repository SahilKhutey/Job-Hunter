import sys
print(sys.path)
try:
    from playwright.async_api import async_playwright
    print("SUCCESS: Playwright is importable")
except ImportError as e:
    print(f"FAILURE: {e}")
