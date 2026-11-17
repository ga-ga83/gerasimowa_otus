import pytest
from playwright.sync_api import Page, Browser, sync_playwright

BASE_URL = "https://www.saucedemo.com/"


@pytest.fixture(scope="session")
def browser():
    """Один браузер на всю сессию — стартует один раз."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True для CI
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser):
    """Свежая вкладка на каждый тест: быстрее запуска браузера, изоляция куки."""
    context = browser.new_context(viewport=None)  # viewport=None → использует размер окна
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})  # аналог maximize_window

    page.goto(BASE_URL)
    yield page

    context.close()
