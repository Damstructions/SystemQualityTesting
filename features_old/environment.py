from playwright.sync_api import sync_playwright

BASE_URL = "https://www.demoblaze.com/"
BASE_URL_OLD = "https://ecommerce-playground.lambdatest.io/"

def before_all(context):
    context.base_url = BASE_URL
    context.pw = sync_playwright().start()
    context.browser = context.pw.chromium.launch(headless=False)  # True for CI

def before_scenario(context, scenario):
    context.page = context.browser.new_page()   # fresh state per scenario

def after_scenario(context, scenario):
    if scenario.status == "failed":
        context.page.screenshot(path=f"screenshots/{scenario.name}.png")
    context.page.close()

def after_all(context):
    context.browser.close()
    context.pw.stop()