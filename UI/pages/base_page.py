"""Базовый класс с общими методами"""

from playwright.sync_api import Page, Locator, expect

DEFAULT_TIMEOUT = 10_000  # миллисекунды

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(DEFAULT_TIMEOUT)

    def find_element(self, selector: str) -> Locator:
        """Элемент с автожиданием появления (до 10 сек)."""
        return self.page.locator(selector)

    def find_elements(self, selector: str) -> list[Locator]:
        """Все подходящие элементы (ждёт хотя бы один)."""
        return self.page.locator(selector).all()

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def get_attribute(self, selector: str, attr: str) -> str | None:
        return self.page.locator(selector).get_attribute(attr)

    def is_element_present(self, selector: str) -> bool:
        """Проверка без ожидания: есть ли элемент в DOM прямо сейчас."""
        return self.page.locator(selector).count() > 0

    def close_password_alert_window(self) -> None:
        selectors = [
            "div[role='alert']",
            "div.notification",
            "div.toast",
        ]

        for selector in selectors:
            for el in self.page.locator(selector).all():
                if "Смените пароль" in (el.inner_text() or ""):
                    self.page.keyboard.press("Escape")
                    return  # закрыли первый подходящий алерт и выходим

    def find_elements_no_wait(self, selector: str) -> list[Locator]:
        """
        Список элементов без ожидания.
        Если элементов нет — пустой список, исключений не бросает.
        """
        locator = self.page.locator(selector)
        try:
            locator.wait_for(state="attached", timeout=1_000)  # 1 секунда
        except Exception:
            return []
        return locator.all()